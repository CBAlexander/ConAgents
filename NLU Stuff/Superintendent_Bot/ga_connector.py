import logging
import json
from sanic import Blueprint, response
from sanic.request import Request
from typing import Text, Optional, List, Dict, Any

from rasa.core.channels.channel import UserMessage, OutputChannel
from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import CollectingOutputChannel

from rasa_sdk.events import AllSlotsReset

logger = logging.getLogger(__name__)

class GoogleConnector(InputChannel):

    @classmethod
    def name(self) -> Text:
        return "google_assistant"

    def blueprint(self, on_new_message):
        
        google_webhook = Blueprint('google_webhook', __name__)

        @google_webhook.route("/", methods=['GET'])
        async def health(request):
            return response.json({"status": "ok"})

        @google_webhook.route("/webhook", methods=['POST'])
        async def receive(request):
            payload = request.json
            intent = payload['inputs'][0]['intent']
            text = payload['inputs'][0]['rawInputs'][0]['query']
            flag = 0
            
            if intent == 'actions.intent.MAIN':
                message = "Hello! How can I help you today?"
                AllSlotsReset()
            else:
                out = CollectingOutputChannel()
                await on_new_message(UserMessage(text, out))
                responses = [m["text"] for m in out.messages]
                message = responses[0]
                if len(responses) != 1:
                    flag = 1
    
            if flag == 0:
                r = {
                    "expectUserResponse": 'true',
                    "expectedInputs": [
                    {
                        "possibleIntents": [
                            {
                                "intent": "actions.intent.TEXT"
                            }
                        ],
                        "inputPrompt": {
                            "richInitialPrompt": {
                                "items": [
                                {
                                    "simpleResponse": {
                                        "textToSpeech": message,
                                        "displayText": message
                                    }
                                }
                                ]
                            }
                        }
                    }
                    ]
                    }
            else:
                r = {
                    "expectUserResponse": 'true',
                    "expectedInputs": [
                    {
                        "possibleIntents": [
                            {
                                "intent": "actions.intent.TEXT"
                            }
                        ],
                        "inputPrompt": {
                            "richInitialPrompt": {
                                "items": [
                                {
                                    "simpleResponse": {
                                        "textToSpeech": message,
                                        "displayText": message
                                    }
                                },
                                {
                                    "basicCard": {
                                        "title": "Resource Booker",
                                        "subtitle": "",
                                        "image": {
                                            "url": "https://www.matthewfrankland.co.uk/images/qr-code.png",
                                            "accessibilityText": "QR Code for Resource Booker"
                                        },
                                        "imageDisplayOptions": "CROPPED"
                                    }
                                }
                                ]
                            }
                        }
                    }
                    ]
                    }

            return response.json(r)
                  
        return google_webhook
