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
        data = { 'employee_forename': re.split( next(tracker.get_latest_entity_values("person"), None), delimiter=" ")[0],
                 'employee_surname': re.split( next(tracker.get_latest_entity_values("person"), None), delimiter=" ")[1]}

        result = requests.post(url=api_endpoint, data=data)
        message = json.load(result)

        dispatcher.utter_message(text=data['employee_forename'] + " " + data['employee_surname'] + " is in " + message['message'])
        return []





