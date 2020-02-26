def prepare_entity(string):
    return string.lower().replace(" ", "_")


def force_pick(nlu_room, room_list, logger=None):
    selection = "FAIL"
    target = nlu_room
    if target is not None:

        # Check whether the name of the room is complete
        # (whether a number is missing)
        incomplete_names = [
            "flex_lab",
            "maker_bay",
            "discovery_zone",
            "inspire_and_collaborate",
        ]
        if target in incomplete_names:
            selection = "INCOMPLETE"
            if logger:
                logger.info("Force pick: \"{}\" -> \"{}\"".format(nlu_room, selection))
            return selection

        digital_lab_list = [
            "digital_lab_zone_a",
            "digital_lab_zone_b",
            "digital_design_laboratory_zone_a",
            "digital_design_laboratory_zone_b"
        ]
        if target in digital_lab_list:
            target = "digital_lab"

        target = target.replace(" ", "_")

        highest_prob = 0

        for room in room_list:
            if room == "discovery_zone":   # For some reason discovery_zone_1 is as discovery_zone is Neo4j
                room = "discovery_zone_1"  # TODO: Fix that in Neo4j
            similarity = similar(target, room)
            if similarity > highest_prob:
                highest_prob = similarity
                selection = room

        if highest_prob < 0.8:
            selection = "UNKNOWN"

    if logger:
        logger.info("Force pick: \"{}\" -> \"{}\"".format(nlu_room, selection))
    return selection


def similar(a, b):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a, b).ratio()


def should_stay_silent(request_data, confidence, logger):
    """Checks whether the last bot is in the middle of room
       clarification process. If so, current bot should stay silent
       (unless confidence is very high).
    """
    if confidence > 0.99987:
        return False
    last_bot = request_data.get("current_state.state.last_bot")
    last_bot_params = request_data.get('current_state.state.bot_states', {}).get(last_bot, {}).get('bot_attributes', {})
    try:
        if last_bot_params['clarification_requested']:
            logger.info("Letting the previous bot finish room clarification process.")
            return True
        return False
    except KeyError:
        return False


def check_previous_response(request_data, bot_name, bot_params, parameter):
    last_bot = request_data.get("current_state.state.last_bot")
    if last_bot == bot_name:
        if bot_params.get(parameter) == 1:
            return True
    return False


def clarify_incomplete_room(incomplete_room, new_room, rooms, user_sentence, logger):
    """ Tries to clarify the room when no number is provided for e.g. flex_lab
    """
    # Try to pick a new room, maybe the user will give a full name this time
    room_name = force_pick(new_room, rooms)

    # User didn't give a full name of a room, check whether at least a number was given
    if room_name in ["FAIL", "INCOMPLETE", "UNKNOWN"]:
        logger.info("Attempting to fix an incomplete location: \"{}\"".format(incomplete_room))
        if "1" in user_sentence or ("one" in user_sentence.lower() and "zone" not in user_sentence.lower()):
            room_name = force_pick("{}_1".format(incomplete_room), rooms)
        elif "2" in user_sentence or "two" in user_sentence.lower():
            room_name = force_pick("{}_2".format(incomplete_room), rooms)

    if room_name in ["FAIL", "INCOMPLETE", "UNKNOWN"]:
        room_name = None
    else:
        logger.info("Room successfully clarified: \"{}\"".format(room_name))
    return room_name


def respond_with_room_list(user_sentence, rooms):
    from grid_nlg.nlg import generate_room_list
    if "yes" in user_sentence or "sure" in user_sentence or "ok" in user_sentence or "yeah" in user_sentence:
        rooms_sentence = generate_room_list(rooms)
        return rooms_sentence
    else:
        return ""


if __name__ == "__main__":
    pass
