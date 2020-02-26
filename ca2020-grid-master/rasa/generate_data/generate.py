import csv
import json
import os
import time

SOURCE_FOLDER = "source"
SOURCE_JSON = os.path.join(SOURCE_FOLDER, "source.json")
SYNONYMS_JSON = os.path.join(SOURCE_FOLDER, "synonyms.json")

EVENT_ROOM_CSV = os.path.join(SOURCE_FOLDER, "event_rooms.csv")
RESOURCE_ROOM_CSV = os.path.join(SOURCE_FOLDER, "resource_rooms.csv")
DIRECTION_ROOM_CSV = os.path.join(SOURCE_FOLDER, "direction_rooms.csv")
# rooms that can be booked via Resource Booker
BOOKING_ROOM_CSV = os.path.join(SOURCE_FOLDER, "booking_rooms.csv")
# following refers to resources in rooms e.g. projector
RESOURCE_CSV = os.path.join(SOURCE_FOLDER, "resource.csv")
OUTPUT = "nlu.md"

def get_csv_list(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        return list(reader)

def get_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def output_with_resource(example, resources, output_file):
    if "{resource}" in example:
        for resource in resources:
            output = example.replace("{resource}", resource[0])
            output_file.write(output)
    else:
        output_file.write(example)

def format__output_example(example, rooms, synonyms_json, resources, output_file):
    header = "  - "
    room_tag = "[{}](room)"
    if "{meridian_time_regex}" in example:
        # example = example.replace("{meridian_time_regex}","[((1[0-2]|0?[1-9])(:([0-5][0-9]))? ([AaPp][Mm]))]")
        example = example.replace("{meridian_time_regex}","11 am")
    if "{time_regex}" in example:
        # example = example.replace("{time_regex}","[((1[0-2]|0?[1-9])(:([0-5][0-9]))?)]")
        example = example.replace("{time_regex}","10")
    if "{room}" in example:
        for room in rooms:
            string_arr = room[0].split("/")
            prefix = ""
            room_name = ""
            if len(string_arr) > 1:
                prefix = string_arr[0] + " "
                room_name = string_arr[1]
            else:
                room_name = string_arr[0]
            output = header+example.replace("{room}",prefix+room_tag.format(room_name))+"\n"
            # check for synonyms
            output_with_resource(output, resources, output_file)
            for syn_roomname in synonyms_json:
                if syn_roomname == room_name:
                    #print("Match! syn_roomname:{} , room_name:{}".format(syn_roomname, room_name))
                    synonyms = synonyms_json.get(syn_roomname)
                    for synonym in synonyms:
                        output = header+example.replace("{room}",room_tag.format(synonym))+"\n"
                        #check what this does and amendements needed
                        output_with_resource(output, resources, output_file)
    else:
        output = header+example+"\n"
        output_with_resource(output, resources, output_file)

def add__synonym_tables(synonyms_json, output):
    row_header = "  - "

    flag = False
    for syn_roomname in synonyms_json:
        if flag:
            output.write("\n")
        elif not flag:
            flag = True
        synonym_header = "## synonym:{}\n".format(syn_roomname)
        output.write(synonym_header)
        synonyms = synonyms_json.get(syn_roomname)
        for synonym in synonyms:
            syn_output = row_header+synonym+"\n"
            output.write(syn_output)


def generate():
    source_json = get_json(SOURCE_JSON)
    synonyms_json = get_json(SYNONYMS_JSON)
    #rooms = get_csv_list(ROOM_CSV)
    event_rooms = get_csv_list(EVENT_ROOM_CSV)
    resource_rooms = get_csv_list(RESOURCE_ROOM_CSV)
    direction_rooms = get_csv_list(DIRECTION_ROOM_CSV)
    booking_rooms = get_csv_list(BOOKING_ROOM_CSV)

    resources = get_csv_list(RESOURCE_CSV)

    with open(OUTPUT, "w") as output:
        output.write("<!--GRID Training Data: Generated @ {}-->\n".format(time.ctime()))
        flag = False
        for intent in source_json:
            if flag:
                output.write("\n")
            elif not flag:
                flag = True
            intent_header = "## intent:{}\n".format(intent)
            output.write(intent_header)
            intent_examples = source_json.get(intent)
            if(intent == "event-request"):
                rooms = event_rooms
            elif(intent == "direction-request" or intent == "location-request"):
                rooms = direction_rooms
            elif(intent == "resource-request"):
                rooms = resource_rooms
            elif(intent == "booking-request"):
                rooms = booking_rooms
            for example in intent_examples:
                format__output_example(example, rooms, synonyms_json, resources, output)
        # now append the synonym look-up tables in md format
        add__synonym_tables(synonyms_json, output)



if __name__ == "__main__":
    generate()
