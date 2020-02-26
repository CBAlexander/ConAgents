# Alana for the GRID building

This repository contains code developed for the Alana chatbot in the GRID project which aimed to place Alana in the GRID building as an intelligent assistant.

## GRID bots

There are three bots designed specifically for the GRID building: directions_bot, events_bot, and resource_bot. There are also separate versions of persona_bot and coherence_bot which were adjusted to the GRID. Find example questions for each of the bots below:

#### Directions Bot
Responds to questions about locations of rooms and directions to them.
- Where is flex lab two?
- How do i get to the boardroom?
- I'm looking for the business and enterprise hub.

#### Events Bot
Responds to questions about events such as lectures or workshops.
- What is on?
- What is happening in flex lab one?
- Is there anything happening in partner suite?

#### Resource Bot
Responds to questions about available computers.
- I need a computer.
- How many PCs are free in inspire and collaborate two?
- Are there any spare computers in creative studio?

#### Persona Bot
Responds to general questions about the GRID building. It is written in AIML so it's easy to add new content.
- What does GRID stand for?
- What are the opening hours?
- Where can I get a cup of coffee?

#### Coherence Bot
Coherence bot responds when the other bots don't generate any answer. It's role is to make sure that Alana always responds with something. The bot responds with a randomly selected driver from the `coherence_bot/data/drivers.py` file. If you want, you can for example add drivers which will advertise the bot you are going to implement.


## Neo4j

Information about how rooms in the GRID building are connected and what events are on is stored in a Neo4j graph database. You need to connect to it in order for the directions_bot, events_bot and resource_bot to work. The connection is established in the `grid_libraries/grid_neo4j/grid_neo4j.py` script. It is for you just to query the database, do not try to alter it in any way. 

_With the current configuration you will probably get "Failed to establish connection" error. A different configuration will be pushed soon._


## Rasa

### Generating data

In order to ensure good confidence for entity extraction (e.g. location entities) it is useful for Rasa if an example is given of each entity in a sentence. In order to create many examples of a sentence with varying entities automatically, there is a script called `generate.py` within the `rasa/generate_data` folder. It expects a file named `source.json` as input. This is a json file with intents as keys, and a list of examples as the value for each intent. Within the source folder there are also csv files containing lists of all room names that the system should expect to hear. There are also synonyms for room names which improve room entity recognition.

In order to add an example sentence to the training data file, you just have to add a new entry to the list with `{room}` within the string, and the sentence will be automatically generated for each entity in the `room.csv` file. Run the script using the following command:

```
python3 generate.py
```

The output will be a file called `nlu.md` which is a training set for Rasa. This must be moved into the `rasa/data` folder replacing the exisiting file (if exists).

### Training

Change directory to the rasa folder and type:

```
rasa train nlu
```

This will look for markdown data files in the data folder, in this case the `nlu.md` one. The model will be trained and stored in the model folder in the rasa directory.

### Server

To run the rasa server type:

```
rasa run --enable-api --port <PORT>
```

This will start the server defaulting to the rest api expecting a json containing:

```
{"text":"user sentence"}
```

### Testing

```
curl -d '{"question":"hello"} -X POST http://localhost:<PORT>/model/parse'
```


## Running the GRID bots

Run the GRID bots the same way as the sample_bot. You can find instructions how to run the sample_bot in Week2_lab_instructions.md file.

Example:

```
curl -X POST -H "Content-Type: application/json" -d '{"user_id":"test-5827465823641856215", "question":"hi", "session_id":"CLI-1100002", "projectId": "CA2020", "overrides": {"BOT_LIST": [{"directions_bot":"<HTTP>"}, {"events_bot":"<HTTP>"}, {"resource_bot":"<HTTP>"}, {"grid_persona_bot":"<HTTP>"}, {"grid_coherence_bot":"<HTTP>"}, {"greetings":"http://b28c735a.ngrok.io"}], "PRIORITY_BOTS":["greetings", "directions_bot", "events_bot", "resource_bot", "grid_persona_bot", "grid_coherence_bot"]}}' http://52.23.135.246:5000
```

Change `<HTTP>` elements to appropriate https addresses generated by ngrok. You will need to run a separate ngrok tunnel for each of the new bots. You can create a `config.yml` file where you specify ports for each of them:

```
tunnels:
    greetings:
        proto: http
        addr: 127.0.0.1:5130
        bind-tls: false
    directions_bot:
        proto: http
        addr: 127.0.0.1:5131
        bind-tls: false
    events_bot:
        proto: http
        addr: 127.0.0.1:5132
        bind-tls: false
    resource_bot:
        proto: http
        addr: 127.0.0.1:5133
        bind-tls: false
    grid_persona_bot:
        proto: http
        addr: 127.0.0.1:5134
        bind-tls: false
    grid_coherence_bot:
        proto: http
        addr: 127.0.0.1:5135
        bind-tls: false
```

Then run:

```
./ngrok start --config=config.yml --all
```

There might be limitations to the number of tunnels you can run over a single ngrok client session. You might have to use multiple ngrok accounts e.g. 3 accounts with 2 tunnels per account.