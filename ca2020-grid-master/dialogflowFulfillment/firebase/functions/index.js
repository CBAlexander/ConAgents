'use strict';
const fetch = require('isomorphic-fetch');

// Import the Dialogflow module from the Actions on Google client library.
const {dialogflow, SimpleResponse} = require('actions-on-google');

// Import the firebase-functions package for deployment.
const functions = require('firebase-functions');

// Instantiate the Dialogflow client.
const app = dialogflow({debug: true});

// Handle the Dialogflow intent.
app.intent('Default Fallback Intent', (conv) => {

  var payload = {"question":`${conv.query}`, "projectId":"GRID", "session_id": conv.id, "user_id": conv.id};

  return fetch("http://52.23.135.246:5000",{
    method: 'post',
    url: `http://52.23.135.246:5000`,
    headers: {
      "Content-type": "application/json" 
    },
    body: JSON.stringify(payload)
  })
    .then((response) => {
    if (response.status < 200 || response.status >= 300) {
      throw new Error(response.statusText);
    } else {
      return response.json();
    }
  })
    .then((json) => {
    conv.ask(new SimpleResponse({
      text: json.result,
      speech: json.result,
    }));
    if (json.result.endsWith("goodbye!")) {
      conv.close();
    }
  });
});

// Handle the Dialogflow intent.
app.intent('Default Welcome Intent', (conv) => {
  });

// Set the DialogflowApp object to handle the HTTPS POST request.
//exports.dialogflowFirebaseFulfillment = functions.https.onRequest(app);
exports.dialogflowFirebaseFulfillment = functions.region('europe-west2').https.onRequest(app);