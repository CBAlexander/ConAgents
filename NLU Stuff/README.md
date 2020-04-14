# How To Run Bots

(Details on Alana yet to be added)

## 1st Terminal Instance

In a Bot folder:
    * rasa train
    * rasa run --enable-api -p 5004

Training should have been done before any commits, thus you should only need to start the Rasa API server using the second command. 'rasa run' acts as the API server between the action server that generates the response and the endpoint.

## 2nd Terminal Instance

* ./ngrok http 5004

ngrok creates a sudo address for your localhost, with an SSL certificate, which google actions needs (and presumably Alana to) to connect to the above RASA server. A different sudo address is generated every time the above command is run and should be updated in a bots action.json file.

## 3rd Terminal Instance

In a Bot folder:
    * rasa run actions

Creates server instance that generates RASA responses. These are then passed back to the API server (above) which sends them to the endpoint (for Google Actions via ga_connector.py).

## 4th Terminal Instance

To push a RASA bot to a Google action use (inintially):
    * ./gactions test --action_package action.json --project convagents-9bdf5
and then to update thereafter:
    * ./gactions update --action_package action.json --project convagents-9bdf5

Will need to first authenticate using a Google developer account. The action will be saved under that account. Any device (i.e. Google Nest) that is signed in to the account the action is saved under will be able to use the given action.
