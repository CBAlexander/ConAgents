from flask import Flask, request
from flask_restful import Api
from argparse import ArgumentParser
from utils import log
from utils.abstract_classes import Bot
from utils.dict_query import DictQuery
import sys
import os

# Get absolute path of two directories up, for other GRID packages.
from os.path import dirname, realpath
filepath = realpath(__file__)
one_up = dirname(dirname(filepath))

# local modules
sys.path.append(os.path.join(one_up, "grid_libraries"))
from grid_neo4j.grid_neo4j import GridNeoConnector
from grid_nlg.nlg import generate_path_sentence, generate_room_list
from grid_nlg.nlg import room_clarification_request, clarification_failure_response
from grid_nlu.nlu import Grid_NLU, NLU_Type, Intent_Type
from grid_functions.helper_functions import force_pick, should_stay_silent, check_previous_response
from grid_functions.helper_functions import clarify_incomplete_room, respond_with_room_list

app = Flask(__name__)
api = Api(app)

BRANCH = "master" #log.get_git_branch()
BOT_NAME = "directions_bot"
LOG_NAME = "grid-directions"

logger = log.get_logger(LOG_NAME)

connector = GridNeoConnector(logger)

parser = ArgumentParser()
parser.add_argument('-p', "--port", type=int, default=5131)
parser.add_argument('-l', '--logfile', type=str, default='logs/' + BOT_NAME + '.log')
parser.add_argument('-cv', '--console-verbosity', default='info', help='Console logging verbosity')
parser.add_argument('-fv', '--file-verbosity', default='debug', help='File logging verbosity')


class DirectionsBot(Bot):
    """Provides direction and location information to grid users.
    Arguments:
        DirectionsBot {Bot (Flask_Restful Resource)} -- [Accepts post requests for direction and location information.]
    Returns:
        [JSON] -- [JSON reponse containing path or location.]
    """
    ERROR_MSG = "Sorry I think I misheard the name of the room. Would you like to hear a list of existing rooms?"

    def __init__(self):
        """Directions Bot constructor
        """
        self.config = ""
        self.logger = logger
        self.connector = connector
        self.rooms = self.connector.get_rooms()
        super(DirectionsBot, self).__init__(bot_name=BOT_NAME)

    def get(self):
        """Overwrite super get function to ensure get requests are ignored.
        """
        pass

    def post(self):
        """Handle post requests from grid_main.py
        Returns:
            [JSON] -- [JSON with response object containing direction path or location, or error message.]
        """
        request_data = request.get_json(force=True)
        request_data = DictQuery(request_data)

        self.config = request_data.get('config')

        user_sentence = request_data.get("current_state.state.input.text")

        grid_nlu = Grid_NLU(NLU_Type.MERCURY, LOG_NAME)
        intent = grid_nlu.process_user_sentence(request_data, self.rooms)

        self.response.bot_params = request_data.get('current_state.state.bot_states', {}).get(BOT_NAME, {}).get('bot_attributes', {})

        try:
            self.logger.debug("Clarification requested: {}".format(self.response.bot_params['clarification_requested']))
        except KeyError:
            pass

        if check_previous_response(request_data, BOT_NAME, self.response.bot_params, "stairs"):
            self.response.lock_requested = True
            self.response.result = self.handle_stairs(request_data)

        elif check_previous_response(request_data, BOT_NAME, self.response.bot_params, "direction"):
            self.response.lock_requested = True
            self.response.result = self.handle_location_direction(request_data)

        elif check_previous_response(request_data, BOT_NAME, self.response.bot_params, "room_list"):
            self.response.lock_requested = True
            self.response.bot_params['room_list'] = 0
            self.response.result = respond_with_room_list(user_sentence, self.rooms)

        elif check_previous_response(request_data, BOT_NAME, self.response.bot_params, "clarification_requested"):
            self.response.lock_requested = True
            self.response.bot_params['clarification_requested'] = 0
            self.response.result = self.handle_room_clarification(intent, user_sentence)

        elif intent.type == Intent_Type.DIRECTION:
            if intent.confidence >= 0.85 and intent.location is not None:
                if should_stay_silent(request_data, intent.confidence, self.logger):
                    self.response.result = ""
                else:
                    self.response.lock_requested = True
                    self.response.result = self.handle_direction(intent)

        elif intent.type == Intent_Type.LOCATION:
            if intent.confidence >= 0.85 and intent.location is not None:
                if should_stay_silent(request_data, intent.confidence, self.logger):
                    self.response.result = ""
                else:
                    self.response.lock_requested = True
                    self.response.result = self.handle_location(intent)

        elif intent.type == Intent_Type.ROOM_LIST:
            if intent.confidence >= 0.85:
                if should_stay_silent(request_data, intent.confidence, self.logger):
                    self.response.result = ""
                else:
                    self.response.lock_requested = True
                    self.response.result = self.handle_room_list(intent)
        else:
            # TODO Help Function
            pass

        return [self.response.toJSON()]

    def handle_stairs(self, request_data):
        self.response.bot_params['stairs'] = 0
        destination = self.response.bot_params.get('destination')
        user_sentence = request_data.get("current_state.state.input.text")
        if "stairs" in user_sentence:
            path_sentence, path_list = self.get_path(destination, True)
            return path_sentence
        else:
            path_sentence, path_list = self.get_path(destination, False)
            return path_sentence

    def handle_location_direction(self, request_data):
        self.response.bot_params['direction'] = 0
        destination = self.response.bot_params.get('direction_location')
        user_sentence = request_data.get("current_state.state.input.text")
        if "yes" in user_sentence or "sure" in user_sentence or "ok" in user_sentence or "yeah" in user_sentence:
            path_sentence, path_list = self.get_path(destination, False)
            return path_sentence
        else:
            return "Ok, is there anything else I can help you with?"

    def get_path(self, location, stairs=True):
        """Gets the path to the location using either the stairs or the elevator.

        Arguments:
            location {String} -- The location to get directions to.

        Keyword Arguments:
            stairs {bool} -- [If true take stairs, else take elevator] (default: {True})

        Returns:
            [String] -- [The path to take]
        """
        path_list = []
        try:
            room_name = force_pick(location, self.rooms, self.logger)

            if room_name == "INCOMPLETE":
                self.response.bot_params['previous_intent'] = "direction"
                path_sentence = self.ask_for_room_clarification(location)

            elif room_name != "UNKNOWN":
                if room_name == "discovery_zone_1":  # For some reason discovery_zone_1 is as discovery_zone is Neo4j
                    room_name = "discovery_zone"     # TODO: Fix that in Neo4j
                path_list = self.connector.find_shortest_path(starting_room="entrance", targeted_room=room_name, stairs=stairs)
                if room_name == "discovery_zone":
                    room_name = "discovery_zone_1"
                self.logger.info(path_list)
                path_sentence = generate_path_sentence(path_list, stairs, self.logger, self.config)

            else:
                path_sentence = "Sorry I do not know where that is, would you like to hear a list of existing rooms?"
                self.response.bot_params['room_list'] = 1
            return path_sentence, path_list
        except Exception as e:
            self.logger.error(e)
            path_sentence = self.ERROR_MSG
            self.response.bot_params['room_list'] = 1
            return path_sentence, path_list

    def handle_direction(self, intent):
        """Handles GRID direction intents.
        Arguments:
            intent {Grid_Intent} -- Accepts Grid_Intent variable.
        Returns:
            String -- The direction string.
        """

        try:
            path_sentence, path_list = self.get_path(intent.location, True)

            if "stairs" in path_list:
                stair_status = self.response.bot_params.get('stairs')
                if stair_status == 0 or stair_status == None:
                    self.response.bot_params['stairs'] = 1
                    self.response.bot_params['destination'] = intent.location
                    return "Would you like to take the stairs or the accessible lift?"

        except Exception as e:
            path_sentence = self.ERROR_MSG
            self.logger.error("HANDLE_DIR_ERR:"+str(e))
        return path_sentence

    def handle_location(self, intent):
        """Handles GRID location intent.
        Arguments:
            intent {Grid_Intent} -- Accepts Grid_Intent variable.
        Returns:
            String -- The location string.
        """
        toilet_rooms = [
            "toilets_1", "toilets_2",
            "accessible_toilet_1", "accessible_toilet_2",
            "shower_1", "shower_2"
        ]
        room_name = force_pick(intent.location, self.rooms, self.logger)

        if room_name == "INCOMPLETE":
            self.response.bot_params['previous_intent'] = "location"
            return self.ask_for_room_clarification(intent.location)

        elif room_name != "FAIL":

            # Let persona give general information about toilets and showers
            # (do not say "toilets 1" or "toilets 2")
            if room_name in toilet_rooms:
                return ""

            # Just say on which floor the specified room is
            try:
                if room_name == "discovery_zone_1":  # For some reason discovery_zone_1 is as discovery_zone is Neo4j
                    room_name = "discovery_zone"     # TODO: Fix that in Neo4j
                path_list = self.connector.find_shortest_path(starting_room="entrance", targeted_room=room_name, stairs=True)
                if room_name == "discovery_zone":
                    room_name = "discovery_zone_1"

                path_string = "The {0} is on the {1} floor. Would you like directions?"
                self.response.bot_params['direction'] = 1
                self.response.bot_params['direction_location'] = room_name

                if "stairs" in path_list:
                    path = path_string.format(room_name, "first")
                else:
                    path = path_string.format(room_name, "ground")
            except Exception as e:
                path = self.ERROR_MSG
                self.logger.error(e)
        else:
            path = self.ERROR_MSG
        return path

    def handle_room_list(self, intent):
        """Handles room list intent
        Arguments:
            intent {Grid_Intent} -- Accepts Grid_Intent variable.
        Returns:
            String -- The response with the list of rooms.
        """
        return generate_room_list(self.rooms)

    def ask_for_room_clarification(self, location):
        self.response.bot_params['clarification_requested'] = 1
        self.response.bot_params['incomplete_location'] = location
        return room_clarification_request(location)

    def handle_room_clarification(self, intent, user_sentence):
        """ Tries to clarify the room when no number is provided for e.g. flex_lab
        """
        # Try to clarify the room
        room_name = clarify_incomplete_room(
                self.response.bot_params['incomplete_location'], intent.location,
                self.rooms, user_sentence, self.logger)

        # Failed to clarify the room, offer a list of rooms
        if not room_name:
            self.response.bot_params['room_list'] = 1
            return clarification_failure_response()

        # Room was clarified successfully, proceed with the user's intent
        intent.location = room_name
        if self.response.bot_params['previous_intent'] == "direction":
            return self.handle_direction(intent)
        elif self.response.bot_params['previous_intent'] == "location":
            return self.handle_location(intent)


if __name__ == "__main__":
    args = parser.parse_args()

    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    log.set_logger_params(BOT_NAME + '-' + BRANCH, logfile=args.logfile,
                          file_level=args.file_verbosity, console_level=args.console_verbosity)

    api.add_resource(DirectionsBot, "/")

    app.run(host="0.0.0.0", port=args.port)
