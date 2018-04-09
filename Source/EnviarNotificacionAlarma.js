var admin = require('firebase-admin');
let fs = require('fs');
var serviceAccount = require('./keyAuthorization/domoticaec3882-firebase-adminsdk-rye8h-493394c76b.json');
admin.initializeApp({
credential: admin.credential.cert(serviceAccount),
databaseURL: 'https://domoticaec3882.firebaseio.com/'
});

let token = fs.readFileSync('token.txt', 'utf-8');
console.log(token)
// This registration token comes from the client FCM SDKs.
var registrationToken = token;

// See the "Defining the message payload" section above for details
// on how to define a message payload.
var payload = {
  notification: {
    title: "ALARMA",
    body: "Alerta de intruso",
    sound: "default"
  }
};

// Set the message as high priority and have it expire after 24 hours.
var options = {
  priority: "high",
  timeToLive: 60 * 60 * 24
};

// Send a message to the device corresponding to the provided
// registration token with the provided options.
admin.messaging().sendToDevice(registrationToken, payload, options)
  .then(function(response) {
    console.log("Mensaje enviado:", response);
    process.exit(0);
  })
  .catch(function(error) {
    console.log("Error, mensaje no enviado:", error);
    process.exit(1);
  });
