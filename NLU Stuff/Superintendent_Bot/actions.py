import requests
import json
import regex as re
import datetime, calendar
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset

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

class ReportIssue(Action):

    def name(self) -> Text:
        return "action_report"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("object") != None:
            data = { 'user': 'dbu319113', 'pass': 'mykgeh-gIzzez-5ginka', 'object': tracker.get_slot("object") }
            response = sendPOST("https://www.matthewfrankland.co.uk/conv-agents/report_issue.php", data, dispatcher)
            if response != False:
                dispatcher.utter_message(text="I have reported your issue to my supervisors. Thank you!!")
        else:
            dispatcher.utter_message(text="Can't find report an issue if you don't tell me what is broken! Lets try again. What's broken?")
        return [AllSlotsReset()]

class RequestHuman(Action):

    def name(self) -> Text:
        return "action_request"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('response')
        data = { 'user': 'dbu319113', 'pass': 'mykgeh-gIzzez-5ginka' }
        response = sendPOST("https://www.matthewfrankland.co.uk/conv-agents/request_human.php", data, dispatcher)
        
        if response != False:
            dispatcher.utter_message(text="A human has been requested and will attend your location shortly.")
        return []

class WipeSlots(Action):

    def name(self) -> Text:
        return "action_wipe_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]
