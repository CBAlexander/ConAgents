from enum import Enum
from utils.utils import log
import sys
import re


class NLU_Type(Enum):
    """ENUM class for selection of NLU.

    Arguments:
        Enum {Super} -- The class to extend.
    """
    HERMIT = 0
    MERCURY = 1


class Intent_Type(Enum):
    """ENUM Class to represent type of GRID intent.

    Arguments:
        Enum {Super} -- The class to extend.
    """
    EVENT = 0
    LOCATION = 1
    DIRECTION = 2
    DIRECTION_RESPONSE = 3
    BOOK = 4
    HELP = 5
    RESOURCE = 6
    NON_GRID = 7
    EMPTY = 8
    ROOM_LIST = 9


class Grid_Intent():
    """Represents a grid intent
    """
    def __init__(self):
        """Grid_Intent constructor

        Arguments:
            original_sentence {String} -- The original user sentence.
        """
        self.type = None
        self.datetime = None
        self.time_grain = None
        self.location = None
        self.person = None
        self.title = None

    def __str__(self):
        return "TYPE: {}, TIME:{}, GRAIN:{}, location:{}, person:{}".format(
            self.type, self.datetime, self.time_grain, self.location,
            self.person, self.title)


class Grid_NLU():
    """Intermediary class to handle switching GRID NLU.
    """
    def __init__(self, nlu_type, log_name):
        """Grid_NLU Constructor.

        Arguments:
            nlu_type {NLU_Type} -- The type of NLU to use for processing.
        """
        self.logger = log.get_logger(log_name)
        self.nlu_type = nlu_type

    def process_user_sentence(self, request_data, rooms):
        user_sentence = request_data.get("current_state.state.input.text")

        if self.nlu_type == NLU_Type.MERCURY:
            rasa_data = request_data.get("current_state.state.nlu.annotations.grid_rasa")
            if rasa_data is None:
                empty_intent = Grid_Intent()
                empty_intent.type = Intent_Type.EMPTY
                return empty_intent
            else:
                return self.process_with_mercury(rasa_data, user_sentence, rooms)
        else:
            print("ERROR: Unknown NLU.")

    def inormalize(self, room):
        """ Applies inverted normalization
        """
        room = room.replace("one", "1").replace("z1", "zone")
        room = room.replace("two", "2").replace("to", "2")
        room = room.replace("2ilet", "toilet").replace("labora2ry", "laboratory")
        return room.replace(" ", "_")

    def fix_room(self, room, user_sentence, rooms):
        """ Fixes missing number in the name of the room
            (when 2 is recognized as "to")
        """
        rooms_broken = [r.strip("_2").replace("_", " ") for r in rooms]
        if room in rooms_broken:
            pattern = r"{}( |_)to".format(room)
            try:
                fixed_room = re.search(pattern, user_sentence).group(0)
            except AttributeError:
                fixed_room = ""
            room = fixed_room if fixed_room else room
        return room

    def process_with_mercury(self, rasa_data, user_sentence, rooms):
        """Process user sentence using the mercury nlu annotations.

        Arguments:
            rasa_data {dict} -- [The rasa data provided by mercury.]
            user_sentence {String} -- The original sentence uttered by the user.

        Returns:
            [Grid_Itent] -- [The constructed grid intent.]
        """
        grid_intent = Grid_Intent()

        name = rasa_data.get("intent.name")
        confidence = rasa_data.get("intent.confidence")
        grid_intent.confidence = confidence

        switcher = {"event-request": Intent_Type.EVENT, "booking-request": Intent_Type.BOOK, "location-request": Intent_Type.LOCATION, "direction-request": Intent_Type.DIRECTION, "rooms-request": Intent_Type.ROOM_LIST, "resource-request": Intent_Type.RESOURCE, "non-grid": Intent_Type.NON_GRID}
        grid_intent.type = switcher.get(name, Intent_Type.HELP)

        self.logger.info("-----------------------------------------------------------------------")
        self.logger.info("INTENT: "+str(grid_intent.type)+", confidence: "+str(confidence))

        entites = rasa_data.gt("entites")

        try:
            for entity in entites:
                etype = entity["entity"]
                if etype == "room":
                    grid_intent.location = self.inormalize(self.fix_room(entity["value"], user_sentence, rooms))
                    self.logger.info("Found room entity: {}".format(grid_intent.location))
                elif etype == "time":
                    # TODO: handle asking about specific time of a day and time intervals
                    # (doesn't work now)
                    ducking_type = entity["additional_info"]["type"]

                    if ducking_type == "value":
                        grid_intent.datetime = entity["value"]
                        grid_intent.time_grain = entity["additional_info"]["grain"]

                    elif ducking_type == "interval":
                        grid_intent.datetime = entity["value"]["from"]
                        #grid_intent.to = entity["value"]["to"]
                        grid_intent.time_grain = entity["additional_info"]["from"]["grain"]

                    # Changes in two lines below prevent the extraction of "two today" as a time entity
                    # from sentences like "What is on in flex lab two today". However, asking about
                    # specific time of a day is not possible now (TODO: think of a better solution).
                    grid_intent.datetime = grid_intent.datetime[:10] + "T00:00:00.000-08:00"
                    grid_intent.time_grain = "day"

                    self.logger.info("Found Time entity: {} Grain:{}".format(grid_intent.datetime, grid_intent.time_grain))
                elif etype == "person":
                    grid_intent.person = entity["value"]
                    self.logger.info("Found Person entity: {}".format(grid_intent.person))

        except Exception as e:
            self.logger.error(e)

        return grid_intent
