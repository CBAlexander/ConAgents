from flask import Flask, request
from flask_restful import Api
from argparse import ArgumentParser
from utils import log
from utils.abstract_classes import Bot
from utils.dict_query import DictQuery
import sys
import os
import datetime
import re

# Get absolute path of two directories up, for other GRID packages.
from os.path import dirname, realpath
filepath = realpath(__file__)
one_up = dirname(dirname(filepath))

# local modules
sys.path.append(os.path.join(one_up, "grid_libraries"))
from grid_neo4j.grid_neo4j import GridNeoConnector
from grid_nlg.nlg import generate_event_sentence, generate_room_list
from grid_nlg.nlg import room_clarification_request, clarification_failure_response
from grid_nlu.nlu import Grid_NLU, NLU_Type, Intent_Type
from grid_functions.helper_functions import force_pick, prepare_entity, should_stay_silent
from grid_functions.helper_functions import check_previous_response, clarify_incomplete_room, respond_with_room_list

app = Flask(__name__)
api = Api(app)

BRANCH = "master" #log.get_git_branch()
BOT_NAME = 'events_bot'
LOG_NAME = "grid-events"

logger = log.get_logger(LOG_NAME)

connector = GridNeoConnector(logger)

parser = ArgumentParser()
parser.add_argument('-p', "--port", type=int, default=5132)
parser.add_argument('-l', '--logfile', type=str, default='logs/' + BOT_NAME + '.log')
parser.add_argument('-cv', '--console-verbosity', default='info', help='Console logging verbosity')
parser.add_argument('-fv', '--file-verbosity', default='debug', help='File logging verbosity')


class EventsBot(Bot):
    """Provides grid users with information about events and handles booking requests.
    Arguments:
        Bot {Bot (Flask_Restful Resource)} -- Custom defined flask restful resource class.
    Returns:
        Response -- JSON response representing event or booking information.
    """
    BOOKING_ERR = "My apologies but I can not yet book rooms, please check again in future for this functionality. Can I help you with anything else?"

    EVENT_ERR = "Sorry, I didn't find any events matching that description. Is there anything else I can help you with?"
    EVENT_ERR_ROOM = "There are no events in the {} today. Can I help you with anything else?"
    EVENT_ERR_ROOM_UNKNOWN = "Sorry, I think I misheard the name of the room. Please try again."

    def __init__(self):
        """Constructor for Events Bot.
        """
        self.config = ""
        self.logger = logger
        self.connector = connector
        self.rooms = self.connector.get_rooms()
        super(EventsBot, self).__init__(bot_name=BOT_NAME)

    def get(self):
        """Overwrites super get method to ensure get requests are ignored.
        """
        pass

    def post(self):
        """Handles Post requests.
        Returns:
            Reponse -- JSON response with the event or booking information.
        """
        request_data = request.get_json(force=True)
        request_data = DictQuery(request_data)

        self.config = request_data.get('config')

        grid_nlu = Grid_NLU(NLU_Type.MERCURY, LOG_NAME)
        intent = grid_nlu.process_user_sentence(request_data, self.rooms)
        input_text = request_data.get('current_state.state.input.text')

        self.response.bot_params = request_data.get('current_state.state.bot_states', {}).get(BOT_NAME, {}).get('bot_attributes', {})

        try:
            self.logger.debug("Clarification requested: {}".format(self.response.bot_params['clarification_requested']))
        except KeyError:
            pass

        if check_previous_response(request_data, BOT_NAME, self.response.bot_params, "room_list"):
            self.response.lock_requested = True
            self.response.bot_params['room_list'] = 0
            self.response.result = respond_with_room_list(input_text, self.rooms)

        elif check_previous_response(request_data, BOT_NAME, self.response.bot_params, "clarification_requested"):
            self.response.lock_requested = True
            self.response.bot_params['clarification_requested'] = 0
            self.response.result = self.handle_room_clarification(intent, input_text)

        elif intent.type == Intent_Type.EVENT:
            if intent.confidence >= 0.97:
                if should_stay_silent(request_data, intent.confidence, self.logger):
                    self.response.result = ""
                else:
                    self.response.lock_requested = True
                    self.response.result = self.handle_event(intent, input_text)

        elif intent.type == Intent_Type.BOOK:
            if intent.confidence >= 0.97:
                if should_stay_silent(request_data, intent.confidence, self.logger):
                    self.response.result = ""
                else:
                    self.response.lock_requested = True
                    self.response.result = self.handle_booking(intent)
        else:
            # TODO implement help function.
            pass

        return [self.response.toJSON()]

    def handle_event(self, intent, input_text):
        """Handles Event Grid_Intent
        Arguments:
            intent {Grid_Intent} -- The Grid_Intent to handle.
        Returns:
            String -- The event information requested.
        """
        self.logger.info("intent: {}".format(intent))

        # Prevent events bot from producing a response when "Heriot" is mentioned
        # (so that it doesn't respond to "tell me about Heriot-Watt")
        if "heriot" in input_text.lower():
            return ""

        # Check for user input which the events_bot shouldn't respond to
        pattern = "(what ).+( (grid|grade)).*( stand for|mean)"
        try:
            if re.search(pattern, input_text):
                self.logger.info("Non-GRID pattern found in the input text. Returning an empty string.")
                return ""
            else:
                self.logger.info("Non-GRID pattern wasn't found in the input text. Proceeding as usual.")
        except Exception as e:
            self.logger.info("Error while searching for the Non-GRID pattern in the input text: {}. Proceeding as usual.".format(e))

        events_by_title = None
        events_by_person = None
        events_by_date = None
        events_by_location = None

        if intent.title is not None:
            events_by_title = self.connector.find_event_given_name('"'+intent.title.title()+'"')
            pass

        if intent.datetime is not None:
            if intent.time_grain == "day":
                date_entity = intent.datetime[:10]
            else:
                date_entity = intent.datetime
            events_by_date = self.connector.find_event_given_date(date_entity)

        location_name = ""
        if intent.location is not None:
            location_name = force_pick(intent.location, self.rooms, self.logger)

            if location_name == "INCOMPLETE":
                self.response.bot_params['previous_intent'] = "event"
                event_response = self.ask_for_room_clarification(intent.location)
                return event_response

            if location_name != "FAIL":
                if location_name == "discovery_zone_1":  # For some reason discovery_zone_1 is as discovery_zone is Neo4j
                    location_name = "discovery_zone"     # TODO: Fix that in Neo4j
                events_by_location = self.connector.find_event_given_room(location_name)
                if location_name == "discovery_zone":
                    location_name = "discovery_zone_1"

        if intent.person is not None:
            person_entity = intent.person.lower().strip()
            events_by_person = self.connector.find_event_given_person(person_entity)

        if intent.title is None and intent.datetime is None and intent.location is None and intent.person is None:
            events_by_date = self.connector.find_event_given_date(datetime.datetime.now().date())

        event_response = None

        try:
            # Encode utf-8 for the Neo4j connector
            for events_list in [events_by_title, events_by_date, events_by_location, events_by_person]:
                if not events_list:
                    continue
                for event in events_list:
                    event[0] = event[0].encode('utf-8') # title
                    event[2] = event[2].encode('utf-8') # description

            # Merge event lists
            title_date_merged = self.connector.merge_event_lists(events_by_title, events_by_date)
            location_person_merged = self.connector.merge_event_lists(events_by_location, events_by_person)
            event_list_merge = self.connector.merge_event_lists(title_date_merged, location_person_merged)
            event_list_filtered = self.connector.remove_old_events(event_list_merge)
            event_list_sorted = sorted(event_list_filtered, key=lambda x: x[3])

            # Decode utf-8 for the final response
            for event in event_list_sorted:
                event = list(event)
                event[0] = event[0].decode('utf-8')
                event[2] = event[2].decode('utf-8')
                event = tuple(event)

            # Generate final response
            event_response = generate_event_sentence(event_list_sorted, 3, self.logger, self.config)
        except Exception as e:
            self.logger.error("EVENT MERGE ERROR:" + str(e))

        if event_response is None:
            if location_name and location_name == "UNKNOWN":
                event_response = self.EVENT_ERR_ROOM_UNKNOWN
            elif location_name and location_name != "FAIL":
                event_response = self.EVENT_ERR_ROOM.format(location_name)
            else:
                event_response = self.EVENT_ERR
        return event_response

    def handle_booking(self, intent):
        """Handles booking requests.
        Arguments:
            intent {Grid_Intent} -- The Grid_Intent to handle.
        Returns:
            String -- The booking response.
        """
        return self.BOOKING_ERR

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
        if self.response.bot_params['previous_intent'] == "event":
            return self.handle_event(intent, user_sentence)
        elif self.response.bot_params['previous_intent'] == "book":
            return self.handle_booking(intent)


if __name__ == "__main__":
    args = parser.parse_args()

    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    log.set_logger_params(BOT_NAME + '-' + BRANCH, logfile=args.logfile,
                          file_level=args.file_verbosity, console_level=args.console_verbosity)

    api.add_resource(EventsBot, "/")

    app.run(host="0.0.0.0", port=args.port)
