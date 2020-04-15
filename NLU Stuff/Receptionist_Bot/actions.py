import requests
import json
import regex as re
import datetime, calendar
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet

def sendPOST(endpoint, data, dispatcher):
    httpResult = requests.post(url=endpoint, data=data)
    if (httpResult.status_code != 200):
        dispatcher.utter_message(text="Sorry, I could not reach the processing server. Please try again later.")
        return False

    jsonResponse = json.loads(httpResult.text)
    if jsonResponse['error'] == True:
        dispatcher.utter_message(text="I encountered a problem. " + jsonResponse['message'])
        return False

    return jsonResponse

class FindPerson(Action):

    def name(self) -> Text:
        return "action_find_person"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("person") != None:
            person = tracker.get_slot("person").split()
            data = { 'user': 'dbu319113', 'pass': 'mykgeh-gIzzez-5ginka', 'employee_forename': person[0], 'employee_surname': person[1] }
            response = sendPOST("https://www.matthewfrankland.co.uk/conv-agents/find_person.php", data, dispatcher)
            if response != False:
                if len(response['message']) == 0:
                    dispatcher.utter_message(text=data['employee_forename'] + " " + data['employee_surname'] + " has not checked in today.")
                else:
                    dispatcher.utter_message(text=data['employee_forename'] + " " + data['employee_surname'] + " last checked in on " + response['message'][0]['last_check_in_date'] + " at " + response['message'][0]['last_check_in_time'] + " in Room " + response['message'][0]['last_check_in_room'] + ".")
        else:
            dispatcher.utter_message(text="Can't find anyone if I don't know who you want to find. Obviously! Lets try again. Who do you want to find?")
        return [AllSlotsReset()]

class SuggestEdit(Action):

    def name(self) -> Text:
        return "action_suggest_edit"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("person") != None:
            data = { 'user': 'dbu319113', 'pass': 'mykgeh-gIzzez-5ginka', 'person': tracker.get_slot("person") }
            response = sendPOST("https://www.matthewfrankland.co.uk/conv-agents/suggest_edit.php", data, dispatcher)
            if response != False: dispatcher.utter_message(text="I will send your suggested update to my system administrators. Thank you!")
        else:
            dispatcher.utter_message(text="Can't send an edit suggestion if you don't tell me who's data is incorrect. Obviously! Lets try again. What edit do you want to suggest?")
        return [AllSlotsReset()]
        
class ProcessBookingRequest(Action):

    def name(self) -> Text:
        return "action_booking"

    def findRoom(self, num_people, date, dispatcher):
        data = { 'user': 'dbu319113', 'pass': 'mykgeh-gIzzez-5ginka', 'num_people': num_people, 'date': date }
        response = sendPOST("https://www.matthewfrankland.co.uk/conv-agents/find_room.php", data, dispatcher)
        if response == False: return False
        return response['message']

    def processDay(self, day_string):
        day = list(calendar.day_name).index(day_string.title())
        today = datetime.date.today()
        return today + datetime.timedelta( (day-today.weekday()) % 7 )

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        amount = "1" if tracker.get_slot("amount") == None else tracker.get_slot("amount")
        date = self.processDay(tracker.get_slot("day").lower()) if tracker.get_slot("day") != None else datetime.date.today()
        bookingFlag = (tracker.get_slot("book_room") != None or amount != None) and tracker.get_slot("cancel_room") == None
        
        if bookingFlag:
            if amount != None and tracker.get_slot("book_room") == None:
                room = self.findRoom(amount, date.strftime("%Y-%m-%d"), dispatcher)
                if room == "": dispatcher.utter_message(text="There are no rooms available for " + amount + " people.")
                if room == False or room == "": return [AllSlotsReset()]
            else:
                room = tracker.get_slot("book_room")
            
            endpoint = "https://www.matthewfrankland.co.uk/conv-agents/book_room.php"
            data = { 'user': 'dbu319113', 'pass': 'mykgeh-gIzzez-5ginka', 'forename': 'User', 'surname': 'Simulated', 'email': 'user@simulated.hw.ac.uk', 'book_date': date.strftime("%Y-%m-%d"), 'book_time': '10:00', 'room_name': room, 'length_min': '840', 'num_people': amount }
        elif tracker.get_slot("cancel_room") != None:
            endpoint = "https://www.matthewfrankland.co.uk/conv-agents/cancel_room.php"
            data = { 'user': 'dbu319113', 'pass': 'mykgeh-gIzzez-5ginka', 'forename': 'User', 'surname': 'Simulated', 'email': 'user@simulated.hw.ac.uk', 'book_date': date.strftime("%Y-%m-%d"), 'book_time': '10:00', 'room_name': tracker.get_slot("cancel_room") }
        else:
            dispatcher.utter_message(text="My processing failed. I am still a work in progress - sorry.")
            return [AllSlotsReset()]
        
        response = sendPOST(endpoint, data, dispatcher)
        if response != False:
            if bookingFlag:
                dispatcher.utter_message(text="I have temporarily reserved room '" + room + "' for you on the " + date.strftime("%d %b, %Y") + ". " + response['message'])
            else:
                dispatcher.utter_message(text="I have temporarily cancelled room '" + tracker.get_slot("cancel_room") + "' which was booked for the " + date.strftime("%d %b, %Y") + ". " + response['message'])
            dispatcher.utter_message(text="Show QR Code")

        return [AllSlotsReset()]

class CheckIn(Action):

    def name(self) -> Text:
        return "action_check_in"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("person") != None and tracker.get_slot("check_in_room") != None:
            data = { 'user': 'dbu319113', 'pass': 'mykgeh-gIzzez-5ginka', 'employee': tracker.get_slot("person"), 'room_name': tracker.get_slot("check_in_room") }
            response = sendPOST("https://www.matthewfrankland.co.uk/conv-agents/employee_check_in.php", data, dispatcher)
            if response != False:
                dispatcher.utter_message(text=tracker.get_slot("person") + " has been checked in to " + tracker.get_slot("check_in_room"))
        else:
            dispatcher.utter_message(text="Can't check in if I don't know who to check in and where to check them into. Obviously! Lets try again. Who and where do you want to check in?")
        return [AllSlotsReset()]

class FindEvents(Action):

    def name(self) -> Text:
        return "action_find_event"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("room") != None:
            data = { 'user': 'dbu319113', 'pass': 'mykgeh-gIzzez-5ginka', 'room_name': tracker.get_slot("room") }
            response = sendPOST("https://www.matthewfrankland.co.uk/conv-agents/future_events.php", data, dispatcher)
            if response != False:
                if len(response['message']) == 0:
                    dispatcher.utter_message(text="No events are currently scheduled in " + tracker.get_slot("room") + ".")
                else:
                    response = tracker.get_slot("room") + " is booked at the following times: "
                    for booking in response['message']:
                        response += booking['date_booked'] + ", "
                    response = response[:-2]
                    dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="I can't give you all the events in the building. Obviously! You must give me a specific room.")
        return [AllSlotsReset()]

class WipeSlots(Action):

    def name(self) -> Text:
        return "action_wipe_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]

class CheckBook(Action):

    def name(self) -> Text:
        return "action_utter_booking"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if "cancel" not in tracker.latest_message['text']:
            if tracker.get_slot("book_room") != None:
                if tracker.get_slot("day") != None and (tracker.get_slot("amount") != None and tracker.get_slot("day") != "1"):
                    dispatcher.utter_message(text="To confirm, I will reserve '" + tracker.get_slot("book_room") + "' on " + tracker.get_slot("day").title() + " for " + tracker.get_slot("amount") + " people?")
                elif tracker.get_slot("day") != None and tracker.get_slot("amount") == None:
                    dispatcher.utter_message(text="To confirm, I will reserve '" + tracker.get_slot("book_room") + "' on " + tracker.get_slot("day").title() + " ?")
                elif tracker.get_slot("day") == None and (tracker.get_slot("amount") != None and tracker.get_slot("amount") != "1"):
                    dispatcher.utter_message(text="To confirm, I will reserve '" + tracker.get_slot("book_room") + "' for today for " + tracker.get_slot("amount") + " people?")
                else:
                    dispatcher.utter_message(text="To confirm, I will reserve '" + tracker.get_slot("book_room") + "' for today for you?")
            else:
                if tracker.get_slot("day") != None and (tracker.get_slot("amount") != None and tracker.get_slot("day") != "1"):
                    dispatcher.utter_message(text="To confirm, I will reserve a free room on " + tracker.get_slot("day").title() + " for " + tracker.get_slot("amount") + " people?")
                elif tracker.get_slot("day") != None and tracker.get_slot("amount") == None:
                    dispatcher.utter_message(text="To confirm, I will reserve a free room on " + tracker.get_slot("day").title() + "?")
                elif tracker.get_slot("day") == None and (tracker.get_slot("amount") != None and tracker.get_slot("amount") != "1"):
                    dispatcher.utter_message(text="To confirm, I will reserve a free room for today for " + tracker.get_slot("amount") + " people?")
                else:
                    dispatcher.utter_message(text="To confirm, you would like me to reserve a free room for today?")
        else:
            if tracker.get_slot("cancel_room") != None:
                if (tracker.get_slot("day") != None and (tracker.get_slot("amount") != None and tracker.get_slot("day") != "1")) or (tracker.get_slot("day") != None and tracker.get_slot("amount") == None):
                    dispatcher.utter_message(text="To confirm, I will cancel room '" + tracker.get_slot("cancel_room") + "' which was booked for " + tracker.get_slot("day").title() + "?")
                else:
                    dispatcher.utter_message(text="To confirm, I will cancel room '" + tracker.get_slot("cancel_room") + "' which was booked for today?")
            else:
                dispatcher.utter_message(text="I can't do anything if you don't give me a room. Obviously! Lets try again. What do you want me to do?")
                return [AllSlotsReset()]
        return []
