# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


#This is a simple example for a custom action which utters "Hello World!"

import requests
import json
import regex as re
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class FindPerson(Action):

    def name(self) -> Text:
        return "action_find_person"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        api_endpoint = "https://www.matthewfrankland.co.uk/conv-agents/find_person.php"
        data = { 'user': 'dbu319113',
                 'pass': 'mykgeh-gIzzez-5ginka',
                 'employee_forename': re.split( next(tracker.get_latest_entity_values("person"), None), delimiter=" ")[0],
                 'employee_surname': re.split( next(tracker.get_latest_entity_values("person"), None), delimiter=" ")[1]}

        result = requests.post(url=api_endpoint, data=data)
        message = json.load(result)

        dispatcher.utter_message(text=data['employee_forename'] + " " + data['employee_surname'] + " is in " + message['message'])
        return []

class DisplayEventsForm(Action):

    def name(self) -> Text:
        return "action_display_booking_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        booking_form_url = "http://portal.hw.ac.uk"
        # open a URL
        return []

class SendEmail(Action):

    def name(self) -> Text:
        return "action_send_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        api_endpoint = "https://www.matthewfrankland.co.uk/conv-agents/suggest_edit.php"
        
        email = next(tracker.get_latest_entity_values("edit_email"), None)
        message = next(tracker.get_latest_entity_values("edit_message"), None)
        
        data = { 'user': 'dbu319113',
                 'pass': 'mykgeh-gIzzez-5ginka',
                 'recipient_email': email,
                 'message': message}
        
        result = requests.post(url=api_endpoint, data=data)
        message = json.load(result)
        
        dispatcher.utter_message(text="Your suggested edit has been sent")
        return []

class FindEvents(Action):

    def name(self) -> Text:
        return "action_find_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        api_endpoint = "https://www.matthewfrankland.co.uk/conv-agents/future_events.php"
        
        room = next(tracker.get_latest_entity_values("event_room"), None)
        building = next(tracker.get_latest_entity_values("event_building"), None)
        
        data = { 'user': 'dbu319113',
                 'pass': 'mykgeh-gIzzez-5ginka',
                 'room_name': room,
                 'building_name': building}
        
        result = requests.post(url=api_endpoint, data=data)
        message = json.load(result)
        
        response = room + " is booked at the following times: ";
        
        for (booking in message) {
            datetimeObj = datetime.strptime(message['date_booked'].'T'.message['time_booked'], '%d %B %Y %H:%M')
            
            response += datetimeObj ", "
        }
        
        response = response[:-1]
        
        dispatcher.utter_message(text=message)
        return []




