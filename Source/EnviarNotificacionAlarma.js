var admin = require('firebase-admin');
var serviceAccount = require('keyAuthorization/domoticaec3882-firebase-adminsdk-rye8h-b14ac69b81.json');
admin.initializeApp({
credential: admin.credential.cert(serviceAccount),
databaseURL: 'https://domoticaec3882.firebaseio.com/'
});
var db = admin.database();

// This registration token comes from the client FCM SDKs.
var registrationToken = "dO7K5jNOlDU:APA91bFAw6c01B22i0XUv3JPGwAHp39LJbmKu5f7jXqmcSoYxko8zoTTYE0UAqY1CGpgAc6zTqmdoX_Cr6oD8WnlukGOS7zIXd3nQOOX0SIKcDuffgrqLZ5PBB2ikqX9DefvlRvVAgiH";

// See the "Defining the message payload" section above for details
// on how to define a message payload.
var payload = {
  notification: {
    title: "ALARMA",
    body: "Alerta de intruso"
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
    console.log("Successfully sent message:", response);
  })
  .catch(function(error) {
    console.log("Error sending message:", error);
  });
 