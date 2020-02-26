from flask import Flask, request
from flask_restful import Api
from argparse import ArgumentParser
from utils import log
from utils.abstract_classes import Bot
from utils.dict_query import DictQuery
from bs4 import BeautifulSoup
#from tidylib import tidy_document
import sys
import os
import requests

# Get absolute path of two directories up, for other GRID packages.
from os.path import dirname, realpath
filepath = realpath(__file__)
one_up = dirname(dirname(filepath))

# local modules
sys.path.append(os.path.join(one_up, "grid_libraries"))
from grid_neo4j.grid_neo4j import GridNeoConnector
from grid_nlg.nlg import generate_pc_sentence, generate_room_list
from grid_nlg.nlg import room_clarification_request, clarification_failure_response
from grid_nlu.nlu import Grid_NLU, NLU_Type, Intent_Type
from grid_functions.helper_functions import force_pick, should_stay_silent, check_previous_response
from grid_functions.helper_functions import clarify_incomplete_room, respond_with_room_list

app = Flask(__name__)
api = Api(app)

BRANCH = "master" #log.get_git_branch()
BOT_NAME = "resource_bot"
LOG_NAME = "grid-resource"

logger = log.get_logger(LOG_NAME)

connector = GridNeoConnector(logger)

parser = ArgumentParser()
parser.add_argument('-p', "--port", type=int, default=5133)
parser.add_argument('-l', '--logfile', type=str, default='logs/' + BOT_NAME + '.log')
parser.add_argument('-cv', '--console-verbosity', default='info', help='Console logging verbosity')
parser.add_argument('-fv', '--file-verbosity', default='debug', help='File logging verbosity')


class ResourceBot(Bot):
    """Provides information on building resources to grid users.
    Arguments:
        ResourceBot {Bot (Flask_Restful Resource)} -- [Accepts post requests for direction and location information.]
    Returns:
        [JSON] -- [JSON reponse containing resource information.]
    """
    ERROR_MSG = "Sorry something went wrong. Is there anything else I can help you with?"

    def __init__(self):
        """Resource Bot constructor
        """
        self.config = ""
        self.logger = logger
        self.connector = connector
        self.rooms = self.connector.get_rooms()
        super(ResourceBot, self).__init__(bot_name=BOT_NAME)

    def get(self):
        """Overwrite super get function to ensure get requests are ignored.
        """
        pass

    def post(self):
        """Handle post requests from grid_main.py
        Returns:
            [JSON] -- [JSON with response object containing direction path or
                       location, or error message.]
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

        if check_previous_response(request_data, BOT_NAME, self.response.bot_params, "room_list"):
            self.response.lock_requested = True
            self.response.bot_params['room_list'] = 0
            self.response.result = respond_with_room_list(user_sentence, self.rooms) 

        elif check_previous_response(request_data, BOT_NAME, self.response.bot_params, "clarification_requested"):
            self.response.lock_requested = True
            self.response.bot_params['clarification_requested'] = 0
            self.response.result = self.handle_room_clarification(intent, user_sentence)

        elif intent.type == Intent_Type.RESOURCE:
            if intent.confidence >= 0.85:
                if should_stay_silent(request_data, intent.confidence, self.logger):
                    self.response.result = ""
                else:
                    self.response.lock_requested = True
                    self.response.result = self.handle_resource(intent)
        else:
            pass

        return [self.response.toJSON()]

    def handle_resource(self, intent):
        resource_response = None
        try:
            page_link = 'http://www.hw.ac.uk/php/lab-availability/labs.php'
            page_response = requests.get(page_link, timeout=5)
            self.soup = BeautifulSoup(page_response.content, 'html.parser')
        except Exception as e:
            self.logger.error("ERROR PARSING WEBPAGE:" + str(e))
            return "My apologies, I can not access resource information at the moment, please try again later."

        # get pc info for all rooms in list
        room_list = [
            "digital_lab",
            "inspire_and_collaborate_1",
            "inspire_and_collaborate_2",
            "flex_lab_1",
            "flex_lab_2"
        ]
        pc_info_list = []
        for room in room_list:
            pc_info = self.get_pc_info(room)
            pc_info_list.append(pc_info)

        # get pc info for the specified room
        pc_info_tpl = ()
        if intent.location is not None:
            location = force_pick(intent.location, self.rooms, self.logger)
            if location == "INCOMPLETE":
                return self.ask_for_room_clarification(intent.location)
            pc_info_tpl = self.get_pc_info(location)

        resource_response = generate_pc_sentence(pc_info_list, pc_info_tpl, self.logger, self.config)
        return resource_response

    def get_pc_info(self, room_name):
        switcher = {
            "digital_lab": "grid digital lab",
            "inspire_and_collaborate_1": "grid learning commons",
            "inspire_and_collaborate_2": "grid learning and collaboration",
            "flex_lab_1": "grid multi flex (ground floor)",
            "flex_lab_2": "grid multi flex (1st floor)"
        }
        hw_location_name = switcher.get(room_name, "grid digital lab")

        results = self.soup.find_all("tr", {"data-sortaz": hw_location_name})

        num_free_int = 0
        total_int = 0

        for result in results:
            num_pcs_str = str(result.find("td", {"class": "pcs"}))
            num_free = num_pcs_str[14:19]
            total = num_pcs_str[32:39]

            num_free_int = int("".join(c for c in num_free if c.isdigit()))
            total_int = int("".join(c for c in total if c.isdigit()))

        return room_name, num_free_int, total_int

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
        return self.handle_resource(intent)


api.add_resource(ResourceBot, "/")

if __name__ == "__main__":
    bot = ResourceBot()
    page_link = 'http://www.hw.ac.uk/php/lab-availability/labs.php'
    page_response = requests.get(page_link, timeout=5)
    bot.soup = BeautifulSoup(page_response.content, 'html.parser')

    args = parser.parse_args()

    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    log.set_logger_params(BOT_NAME + '-' + BRANCH, logfile=args.logfile,
                          file_level=args.file_verbosity, console_level=args.console_verbosity)

    api.add_resource(ResourceBot, "/")

    app.run(host="0.0.0.0", port=args.port)
