import sys
from datetime import datetime
from dateutil.parser import parse
from pytz import timezone
from collections import OrderedDict
from utils import log
import operator
import random


DRIVERS = {
    "general": [
        " Is there anything else I can help you with?",
        " Can I help you with anything else?",
        " What else can I help you with?",
        " What else would you like to know?",
        " Is there anything else you'd like to know?",
        " If there's anything else you'd like to know, just ask.",
        " Let me know if I can help you with anything else.",
        ""
    ],
    "alana_topics": [
        "{0} you can talk to me about things like movies, sports, news, and music{1}",
        "{0} I can chat about almost anything{1}",
        "{0} you can have a conversation with me about any topic, like news, music, or your favourite movie{1}",
        "{0} you can talk to me about lots of things, like movies or music or the news{1}",
        "{0} we can also discuss current news, sports and movies{1}",
        "{0} you can talk to me about movies, music and current news{1}",
        "{0} I can also talk about books or movies{1}",
        "{0} I can also talk about sports or music{1}",
        "{0} we can have a chat about many topics such as music and movies{1}",
        "{0} we can chat about various things like movies, sports or current news{1}",
        "{0} I like to talk about movies{1} The Wizard of Oz is one of my favourites.",
        "{0} I like chatting about music{1} I admire Taylor Swift!",
        "{0} I can provide you with current news{1} Just ask me for the news headlines.",
        "{0} I fancy chatting about books and sports as well{1}",
        "{0} you can have a chat with me about many topics like movies and sports{1}"
    ],
    "directions": [
        "{0} if you're looking for a specific room, you can ask me how to get there{1}",
        "{0} you can ask me about directions to rooms in this building{1}",
        "{0} I can give you directions to any room in this building{1} Just ask."
    ],
    "events": [
        "{0} if you're interested in attending some events, you can ask me what is on today{1}",
        "{0} you can ask me about events happening in this building{1}",
        "{0} you can ask me what events are on in this building{1}"
    ],
    "resources": [
        "{0} if you need a computer, you can ask me where you can find an available one{1}",
        "{0} if you need a computer, I can tell you where to find a free one{1} Just ask.",
        "{0} you can ask me about available computers{1}",
        "{0} you can ask me whether there are any computers free{1}"
    ]
}
OPENINGS = [
    (" By the way, ", "."),
    (" Do you know that ", "?"),
    (" Did you know that ", "?"),
    (" Don't forget that ", "."),
    (" In case you don't know, ", "."),
    (" In case you didn't know, ", "."),
    (" In case you forgot, ", "."),
    (" I hope you know that ", "."),
    (" I hope you remember that ", ".")
]
RESOURCE_ROOMS = [
    "inspire_and_collaborate_1",
    "inspire_and_collaborate_2",
    "flex_lab_1",
    "flex_lab_2",
    "gaming_studio",
    "digital_lab",
    "digital_lab_zone_a",
    "digital_lab_zone_b"
]


def add_driver(output_sentence, dont_mention, logger, config):
    """Adds a driver to the end of the output sentence

    Arguments:
        output_sentence {string} -- the generated output sentence

        dont_mention {string} -- either 'directions' or 'events' or 'resources'
                                 (So that we don't advertise a functionality
                                  that the user has just used.)
        logger {logging.Logger} -- logger to be used
        config {string} -- configuration of the system, either 'grid_alana' or 'grid_only'

    Returns:
        string -- the generated output sentence with a driver
    """
    # Don't add a driver to an empty output sentence
    if not output_sentence:
        return output_sentence

    # Create a filtered list of drivers
    dont_mention = [dont_mention]
    if config == "grid_only":
        dont_mention.extend(["alana_topics", "directions", "events", "resources"])
    logger.info("Topics not to mention: {}".format(", ".join(dont_mention)))
    drivers = sum([DRIVERS[key] for key in DRIVERS.keys() if key not in dont_mention], [])

    # Choose a driver randomly and format it with a random opening
    opening = random.choice(OPENINGS)
    driver = random.choice(drivers).format(opening[0], opening[1])

    return output_sentence + driver


def generate_path_sentence(output_list, stairs, logger, config):
    """generate a sentence from a given list of areas

    Arguments:
        output_list {list} -- output from Neo4J of the path to use
        stairs {bool} -- [If true take stairs, else take elevator]
        logger {logging.Logger} -- logger to be used
        config {string} -- configuration of the system, either 'grid_alana' or 'grid_only'

    Returns:
        string -- the generated sentence
    """
    # this is the output of the functions
    output_sentence = ""

    # for each elements
    for index, area in enumerate(output_list):

        next = ""
        if index+1 < len(output_list):
            next = output_list[index+1]

        if area == "entrance":
            output_sentence += "From the entrance,"

        if (area == "atrium") and (next == "stairs"):
            output_sentence += " head across the atrium and take the stairs"

        if (area == "atrium") and (next == "accessible_lift"):
            output_sentence += " head across the atrium to the right and take the accessible lift to the first floor"

        if (area == "atrium") and (next == "inspire_and_collaborate_1"):
            output_sentence += " turn right, inspire and collaborate 1 is in front of you."

        if (area == "atrium") and (next == "flex_lab_1"):
            output_sentence += " turn left, flex lab 1 will be in front of you."

        if (area == "flex_lab_1") and (next == "maker_bay_1"):
            output_sentence += " Get inside. Maker bay 1 is the area without computers."

        if (area == "flex_lab_1") and (next == "discovery_zone"):        # For some reason discovery_zone_1 is as discovery_zone is Neo4j
            output_sentence += " Discovery zone 1 is inside that room."  # TODO: Fix that in Neo4j

        if (area == "flex_lab_1") and (next == "discovery_zone_1"):
            output_sentence += " Discovery zone 1 is inside that room."

        if (area == "atrium") and (next == "zone_0_2"):
            output_sentence += " head across the atrium while keeping to the left of the stairs"

        if area == "cafe":
            output_sentence += ". It looks like a tuck tuck."

        if (area == "atrium") and (next == "accessible_toilet_1"):
            output_sentence += " head across the atrium to the right, the accessible toilet is here."

        if (area == "atrium") and (next == "zone_0_1"):
            output_sentence += " head across the atrium to the right."

        if (area == "zone_0_2") and (next == "inspire_and_collaborate_2"):
            output_sentence += ", once past them please turn right, inspire and collaborate 2 will be in front of you."

        if (area == "zone_0_2") and (next == "shower_1"):
            output_sentence += ", enter the door on the left marked toilets, the shower is the first room on the left."

        if (area == "zone_0_2") and (next == "toilets_1"):
            output_sentence += ", enter the door on the left marked toilets."

        if (area == "zone_0_3") and (next == "creative_studio"):
            output_sentence += ", head to the back of the building, the creative studio is the last door on the right hand side."

        if (area == "zone_0_3") and (next == "zone_0_4"):
            output_sentence += ", head to the back of the building, and enter the second last door on the left."

        if (area == "zone_0_3") and (next == "gaming_studio"):
            output_sentence += ", head to the back of the building, the gaming studio is the last door on the left."

        if (area == "zone_0_4") and (next == "maths_gym"):
            output_sentence += " The maths gym is the first door on the left."

        if (area == "zone_0_4") and (next == "management_and_support_centre"):
            output_sentence += " The management and support centre is the door at the end of the corridor."

        if (area == "inspire_and_collaborate_1") and ("meeting_room" in next):
            output_sentence += " Enter the room, turn left and the meeting rooms are on the back wall."

        if (area == "inspire_and_collaborate_2") and ("meeting_room" in next):
            output_sentence += " Enter the room and the meeting rooms are the glass rooms adjacent to the door."

        if area == "zone_1_5" and (next == "zone_1_1"):
            output_sentence += ", then turn right"

        if area == "zone_1_1" and (next == "zone_1_2"):
            output_sentence += " and go past the stairs"

        if area == "zone_1_1" and (next == "digital_lab"):
            output_sentence += ", the door to the digital lab will be in front of you."

        if area == "stairs" and (next == "zone_1_1"):
            output_sentence += ", at the top turn left"

        if area == "stairs" and (next == "zone_1_2"):
            output_sentence += ", at the top turn right"

        if area == "zone_1_2" and (next == "flex_lab_2"):
            output_sentence += " and flex lab 2 will be in front of you."

        if area == "flex_lab_2" and (next == "maker_bay_2"):
            output_sentence += " Get inside. Maker bay 2 is the area without computers."

        if area == "flex_lab_2" and (next == "discovery_zone_2"):
            output_sentence += " Discovery zone 2 is inside that room."

        if area == "flex_lab_2" and (next == "faraday_cage"):
            output_sentence += " Get inside. Faraday cage is at the back of that room."

        if area == "zone_1_3":
            output_sentence += " and proceed to the back of the building"

        if area == "zone_1_3" and (next == "imagineering_suite"):
            output_sentence += ", the imagineering suite is the last door on the left."

        if (area == "zone_1_3") and (next == "shower_2"):
            output_sentence += ", enter the door on the left marked toilets, the shower is the first room on the left."

        if (area == "zone_1_3") and (next == "toilets_2"):
            output_sentence += ", enter the door on the left marked toilets."

        if area == "zone_1_4":
            output_sentence += " and enter the second last door on the left"

        if area == "boardroom":
            output_sentence += ", the boardroom is at the end of the corridor."

        if area == "partner_suite":
            output_sentence += ", the partner suite is then the first door on the left."

        if area == "business_and_enterprise_hub":
            output_sentence += ", the business and enterprise hub will be located on your right."

        if (area == "business_and_enterprise_hub") and ("meeting_room" in next):
            output_sentence += " Enter the room and the meeting rooms are along the wall adjacent to the doors."

        if area == "zone_1_5" and (next == "accessible_toilet_2"):
            output_sentence += ", exit and turn left, the toilet is here."

        if area == "vending_machine":
            output_sentence += " The vending machine is next to the stairs."

        if area == "entrance" and output_list[-1] == "atrium":
            output_sentence = "The atrium is the area you are in when you enter this building."

    return add_driver(output_sentence, "directions", logger, config)


def generate_event_sentence(output_list, number_of_output, logger, config):
    """generate a sentence from a given list of events - tuples containing
       (title, location, description, start, end)

    Arguments:
        output_list {list} -- output from Neo4J of the path to use
        number_of_output {int} -- number of event to return to the user
          (ex: only say the two future events)(curently set to 3 in events bot)
        logger {logging.Logger} -- logger to be used
        config {string} -- configuration of the system, either 'grid_alana' or 'grid_only'

    Returns:
        string -- the generated sentence
    """
    whole_output_sentence = None
    one_location = True

    more_detailed_info = "For more details you can ask me what events are on in a specific room. "

    if output_list is not None:

        # For some reason discovery_zone_1 is as discovery_zone is Neo4j
        # TODO: Fix that in Neo4j
        new_output_list = []
        for event in output_list:
            if event[1] == "discovery_zone":
                event[1] = "discovery_zone_1"
            new_output_list.append(event)
        output_list = new_output_list

        # check whether all events are in the same location
        # if not, give a summary answer
        prev_location = None
        for event in output_list:
            if prev_location and event[1] != prev_location:
                one_location = False
                break
            prev_location = event[1]

        if one_location:
            # all events are in the same location
            # generate event sentence for this location
            return generate_event_sentence_for_one_location(output_list, number_of_output, logger, config)
        else:
            # give a summary answer (number of events by location)
            # first, count events by rooms
            summary = {}
            for event in output_list:
                if event[1] in summary.keys():
                    summary[event[1]] += 1
                else:
                    summary[event[1]] = 1

            # if summary is too long, utter just the total number of events
            if len(summary) > 3:
                all_events_no = sum(summary.values())
                whole_output_sentence = (
                    "The GRID is a busy place! Today there are "
                    + "{0} events happening across {1} ".format(all_events_no, len(summary))
                    + "different rooms. " + more_detailed_info)
                return whole_output_sentence

            # sort by the number of events
            summary_ordered = OrderedDict(sorted(summary.items(), key=lambda x: x[1], reverse=True))

            # utter the summary
            i = 0
            for location, events_no in summary_ordered.items():
                if i == 0:
                    if events_no == 1:
                        whole_output_sentence = "Today there is 1 event taking place in {}. ".format(location)
                    else:
                        whole_output_sentence = "Today there are {0} events taking place in {1}. ".format(events_no, location)
                    i += 1
                elif i == len(summary)-1:
                    whole_output_sentence += "and {} in {}. ".format(events_no, location)
                else:
                    whole_output_sentence += "{} in {}, ".format(events_no, location)
                    i += 1

            whole_output_sentence += more_detailed_info

    return add_driver(whole_output_sentence, "events", logger, config)


def generate_event_sentence_for_one_location(output_list, number_of_output, logger, config):
    """generate a sentence from a given list of events - tuples containing
       (title, location, description, start, end)

    Arguments:
        output_list {list} -- output from Neo4J of the path to use
        number_of_output {int} -- number of event to return to the user
          (ex: only say the two future events)(curently set to 3 in events bot)
        logger {logging.Logger} -- logger to be used
        config {string} -- configuration of the system, either 'grid_alana' or 'grid_only'

    Returns:
        string -- the generated sentence
    """
    output_sentence = None

    # avoid out of index
    if number_of_output >= len(output_list):
        number_of_output = len(output_list)

    for pos in range(number_of_output):
        event = output_list[pos]

        title = event[0]
        location = event[1]
        description = event[2]
        start = parse(event[3])
        end = parse(event[4])

        ukZone = timezone('Europe/London')
        start = start.astimezone(ukZone)
        end = end.astimezone(ukZone)

        if start.date() == datetime.today().date():
            starttime = start.strftime("%H:%M")
        else:
            starttime = start.strftime("%d %B at %H:%M")

        if end.date() == datetime.today().date() or end.date() == start.date():
            endtime = end.strftime("%H:%M")
        else:
            endtime = end.strftime("%d %B at %H:%M")

        if output_sentence is None:
            if number_of_output == 1:
                output_sentence = "There is one event taking place in the {} today. ".format(location)
            else:
                output_sentence = "There are {} events taking place in the {} today. ".format(len(output_list), location)
                if len(output_list) > number_of_output:
                    output_sentence += "Here are the {} coming up next. ".format(number_of_output)  # make sure they're sorted
            output_sentence += "An event called {} {} is scheduled from {} until {}. ".format(title, description, starttime, endtime)
        else:
            if pos == number_of_output-1 and number_of_output > 2:
                output_sentence += "Finally, an event called {} {} is scheduled from {} until {}. ".format(title, description, starttime, endtime)
            else:
                output_sentence += "Another event called {} {} is taking place from {} until {}. ".format(title, description, starttime, endtime)

    return add_driver(output_sentence, "events", logger, config)


def generate_pc_sentence(output_list, output_tpl, logger, config):
    """generate a sentence from a given list of tuples containting
       (room_name, available_pcs, total_pcs)

    Arguments:
        output_list {list} -- output from beautiful soup with numbers of
                              available pcs in all rooms

        output_tpl {tuple} -- (room_name, num_free, num_total) tuple for
                              the room that the user specified in their
                              resource request

        logger {logging.Logger} -- logger to be used
        config {string} -- configuration of the system, either 'grid_alana' or 'grid_only'

    Returns:
        string -- the generated sentence
    """
    output_sentence = ""

    # prepare error_output_sentence for when the room is not specified
    # or other exceptions occur:
    # sort by descending order of PCs avail, read out only the room with
    # the most (assumes at least one free in building)
    output_list.sort(key=operator.itemgetter(1), reverse=True)
    error_output_sentence = (
        " The room {} has the most free computers, ".format(output_list[0][0])
        + "it has {} PCs available. ".format(output_list[0][1])
    )

    if output_tpl:
        # user specified the room

        # For some reason discovery_zone_1 is as discovery_zone is Neo4j
        # TODO: Fix that in Neo4j
        if output_tpl[0] == "discovery_zone":
            output_list = list(output_tpl)
            output_list[0] = "discovery_zone_1"
            output_tpl = tuple(output_list)

        if output_tpl[0] == "UNKNOWN":
            # the name of the room wasn't recognized as any of the grid rooms
            output_sentence += (
                "Sorry, I must have misheard the name of the room you asked "
                + "about, but I know that {}".format(error_output_sentence)
            )
        elif output_tpl[0] not in RESOURCE_ROOMS:
            # user requested a room which does not offer computers
            output_sentence += (
                "Sorry, there are no computers in the "
                + "{0}, but I know that {1}".format(
                    output_tpl[0],
                    error_output_sentence
                )
            )
        elif output_tpl[1] == 0:
            # there are currently no available computers
            # in the requested room
            output_sentence += (
                "I'm afraid there are no free computers in "
                + "{0} at the moment, but I know that {1}".format(
                    output_tpl[0],
                    error_output_sentence)
            )
        else:
            output_sentence += "The room {0} has {1} PCs left, out of {2}.".format(
                output_tpl[0],
                output_tpl[1],
                output_tpl[2]
            )
    else:
        # user didn't ask for a specific room
        output_sentence += error_output_sentence

    return add_driver(output_sentence, "resources", logger, config)


def generate_room_list(room_list):
    """generate a sentence from a list of rooms

    Arguments:
        room_list {list}

    Returns:
        string -- generated list of rooms
    """
    output_sentence = "This building has the following rooms: "

    for room in room_list:
        if "atrium" not in room and "entrance" not in room and "meeting" not in room and "toilet" not in room and "shower" not in room and "vending" not in room and "water" not in room and "stairs" not in room and "lift" not in room and not room.startswith("zone"):

            # For some reason discovery_zone_1 is as discovery_zone is Neo4j
            # TODO: Fix that in Neo4j
            if room == "discovery_zone":
                room = "discovery_zone_1"

            output_sentence += "{}, ".format(room)

    output_sentence = output_sentence[:-2]
    output_sentence += ". There are also 12 meeting rooms."

    return output_sentence


def room_clarification_request(location):
    return "Sorry, there is {0} one and {0} two in this building. Which one do you mean?".format(location)


def clarification_failure_response():
    return "Sorry, I still don't know what room you mean. Would you like to hear a list of existing rooms?"


if __name__ == '__main__':
    #####################################################
    #                   Test input                      #
    #####################################################

    # GROUND FLOOR
    ic1 = ['entrance', 'atrium', 'inspire_and_collaborate_1']

    meeting_room1_4 = ['entrance', 'atrium', 'inspire_and_collaborate_1', 'meeting_room_1_1']

    ic2 = ['entrance', 'atrium', 'zone_0_2', 'inspire_and_collaborate_2']

    meeting_room5_7 = ['entrance', 'atrium', 'zone_0_2', 'inspire_and_collaborate_2', 'meeting_room_1_5']

    creative_studio = ['entrance', 'atrium', 'zone_0_2', 'zone_0_3', 'creative_studio']

    flex1 = ['entrance', 'atrium', 'flex_lab_1']

    maths_gym = ['entrance', 'atrium', 'zone_0_2', 'zone_0_3', 'zone_0_4', 'maths_gym']

    gaming_studio = ['entrance', 'atrium', 'zone_0_2', 'zone_0_3', 'gaming_studio']

    management = ['entrance', 'atrium', 'zone_0_2', 'zone_0_3', 'zone_0_4', 'management_and_support_centre']

    accessible_toilet = ['entrance', 'atrium', 'accessible_toilet_1']

    shower1 = ['entrance', 'atrium', 'zone_0_2', 'shower_1']

    toilets1 = ['entrance', 'atrium', 'zone_0_2', 'toilets_1']

    # FIRST FLOOR --------------------------------------------------------------------------------------------------------------------------

    digital_lift = ['entrance', 'atrium', 'accessible_lift', 'zone_1_5', 'zone_1_1', 'digital_lab']
    digital_stairs = ['entrance', 'atrium', 'stairs', 'zone_1_1', 'digital_lab']

    shower2_lift = ['entrance', 'atrium', 'accessible_lift', 'zone_1_5', 'zone_1_1', 'zone_1_2', 'zone_1_3', 'shower_2']
    shower2_stairs = ['entrance', 'atrium', 'stairs', 'zone_1_2', 'zone_1_3', 'shower_2']

    toilets2_lift = ['entrance', 'atrium', 'accessible_lift', 'zone_1_5', 'zone_1_1', 'zone_1_2', 'zone_1_3', 'toilets_2']
    toilets2_stairs = ['entrance', 'atrium', 'stairs', 'zone_1_2', 'zone_1_3', 'toilets_2']

    accessible_toilet2_lift = ['entrance', 'atrium', 'accessible_lift', 'zone_1_5', 'accessible_toilet_2']
    accessible_toilet2_stairs = ['entrance', 'atrium', 'stairs', 'zone_1_1', 'zone_1_5', 'accessible_toilet_2']

    flex2_lift = ['entrance', 'atrium', 'accessible_lift', 'zone_1_5', 'zone_1_1', 'zone_1_2', 'flex_lab_2']
    flex2_stairs = ['entrance', 'atrium', 'stairs', 'zone_1_2', 'flex_lab_2']

    business_lift = ['entrance', 'atrium', 'accessible_lift', 'zone_1_5', 'zone_1_1', 'zone_1_2', 'zone_1_3', 'business_and_enterprise_hub']
    business_stairs = ['entrance', 'atrium', 'stairs', 'zone_1_2', 'zone_1_3', 'business_and_enterprise_hub']

    meeting_room_2_stairs = ['entrance', 'atrium', 'stairs', 'zone_1_2', 'zone_1_3', 'business_and_enterprise_hub', 'meeting_room_2_2']

    imagineering_lift = ['entrance', 'atrium', 'accessible_lift', 'zone_1_5', 'zone_1_1', 'zone_1_2', 'zone_1_3', 'imagineering_suite']
    imagineering_stairs = ['entrance', 'atrium', 'stairs', 'zone_1_2', 'zone_1_3', 'imagineering_suite']

    boardroom_lift = ['entrance', 'atrium', 'accessible_lift', 'zone_1_5', 'zone_1_1', 'zone_1_2', 'zone_1_3', 'zone_1_4', 'boardroom']
    boardroom_stairs = ['entrance', 'atrium', 'stairs', 'zone_1_2', 'zone_1_3', 'zone_1_4', 'boardroom']

    partner_suite_stairs = ['entrance', 'atrium', 'stairs', 'zone_1_2', 'zone_1_3', 'zone_1_4', 'partner_suite']
    partner_suite_lift = ['entrance', 'atrium', 'accessible_lift', 'zone_1_5', 'zone_1_1', 'zone_1_2', 'zone_1_3', 'zone_1_4', 'partner_suite']

    vending = ['entrance', 'atrium', 'zone_0_1', 'vending_machine']

    # -------------------------------------------------------------------------------------------------------------------------------------
    path_sen = generate_path_sentence(vending, True)

    print(path_sen)
