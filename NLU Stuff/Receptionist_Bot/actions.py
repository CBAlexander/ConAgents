# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


#This is a simple example for a custom action which utters "Hello World!"

import requests
import json
import regex as re
from datetime import datetime
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

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
        
        return [SlotSet("person", None)]

class DisplayEventsForm(Action):

    def name(self) -> Text:
        return "action_display_booking_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # open book_form_url URL
        booking_form_url = "http://portal.hw.ac.uk"

        # noted in database only to simulate a response
        # book_date, book_time and length_min are all given on booking_form
        """
        api_endpoint = "https://www.matthewfrankland.co.uk/conv-agents/book_room.php"
        data = { 'user': 'dbu319113',
                 'pass': 'mykgeh-gIzzez-5ginka',
                 'employee_forename': re.split( next(tracker.get_latest_entity_values("person"), None), delimiter=" ")[0],
                 'employee_surname': re.split( next(tracker.get_latest_entity_values("person"), None), delimiter=" ")[1],
                 'email': next(tracker.get_latest_entity_values("email"), None),
                 'room_name': next(tracker.get_latest_entity_values("room"), None),
                 'building_name': next(tracker.get_latest_entity_values("building"), None),
                 'book_date': '2020-04-29',
                 'book_time': '00:00',
                 'length_min': '20'}
        
        result = requests.post(url=api_endpoint, data=data)
        message = json.load(result)
        """

        dispatcher.utter_message(text="Please enter your booking details on this form")
        """dispatcher.utter_message(text="Your booking has been processed. A confirmation email will be sent to you")"""
        
        """return [SlotSet("person", None), SlotSet("email", None), SlotSet("room", None), SlotSet("building", None)]"""
        return []

class CancelBooking(Action):

    def name(self) -> Text:
        return "action_cancel_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # open canel_booking_form_url URL
        canel_booking_form_url = "http://portal.hw.ac.uk"
        
        # noted in database only to simulate a response
        # book_date, book_time are all taken from event selected to cancel on cancel_booking_form
        """
        api_endpoint = "https://www.matthewfrankland.co.uk/conv-agents/cancel_room.php"
        data = { 'user': 'dbu319113',
                 'pass': 'mykgeh-gIzzez-5ginka',
                 'employee_forename': re.split( next(tracker.get_latest_entity_values("person"), None), delimiter=" ")[0],
                 'employee_surname': re.split( next(tracker.get_latest_entity_values("person"), None), delimiter=" ")[1],
                 'email': next(tracker.get_latest_entity_values("email"), None),
                 'room_name': next(tracker.get_latest_entity_values("room"), None),
                 'building_name': next(tracker.get_latest_entity_values("building"), None),
                 'book_date': '2020-04-29',
                 'book_time': '00:00'}

        result = requests.post(url=api_endpoint, data=data)
        message = json.load(result)
        """

        dispatcher.utter_message(text="Please select your booking on this webpage")
        """dispatcher.utter_message(text="Your booking has been cancelled. A confirmation email will be sent to you")"""
        
        """return [SlotSet("person", None), SlotSet("email", None), SlotSet("room", None), SlotSet("building", None)]"""
        return []

class SendEmail(Action):

    def name(self) -> Text:
        return "action_send_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        api_endpoint = "https://www.matthewfrankland.co.uk/conv-agents/suggest_edit.php"
        data = { 'user': 'dbu319113',
                 'pass': 'mykgeh-gIzzez-5ginka',
                 'recipient_email': next(tracker.get_latest_entity_values("email"), None),
                 'message': next(tracker.get_latest_entity_values("message"), None)}
        
        result = requests.post(url=api_endpoint, data=data)
        message = json.load(result)
        
        dispatcher.utter_message(text="Your suggested edit has been sent")
        
        return [SlotSet("email", None), SlotSet("message", None)]
        
        
class CheckIn(Action):

    def name(self) -> Text:
        return "action_check_in"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        api_endpoint = "https://www.matthewfrankland.co.uk/conv-agents/employee_check_in.php"
        data = { 'user': 'dbu319113',
                 'pass': 'mykgeh-gIzzez-5ginka',
                 'employee_email': next(tracker.get_latest_entity_values("email"), None),
                 'room_name': next(tracker.get_latest_entity_values("room"), None),
                 'building_name': next(tracker.get_latest_entity_values("building"))}
        
        requests.post(url=api_endpoint, data=data)
        
        dispatcher.utter_message(text="Your checked in to this location")
        
        return [SlotSet("email", None), SlotSet("room", None), SlotSet("building", None)]

class FindEvents(Action):

    def name(self) -> Text:
        return "action_find_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        api_endpoint = "https://www.matthewfrankland.co.uk/conv-agents/future_events.php"
        room = next(tracker.get_latest_entity_values("room"), None)
        building = next(tracker.get_latest_entity_values("building"), None)

        data = { 'user': 'dbu319113',
                 'pass': 'mykgeh-gIzzez-5ginka',
                 'room_name': room,
                 'building_name': building}
        result = requests.post(url=api_endpoint, data=data)
        message = json.load(result)
        
        response = room + " is booked at the following times: "
        
        for booking in message:
            response += datetime.strptime(booking['date_booked'] + "T" + booking['time_booked'], '%Y-%m-%dT%H:%M:%S').strftime('%d %B %Y %H:%M') + ", "
        
        response = response[:-2]
        
        dispatcher.utter_message(text=message)

        return [SlotSet("room", None), SlotSet("building", None)]




