import firebase_admin
import time
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('domoticaec3882-firebase-adminsdk-rye8h-493394c76b.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://domoticaec3882.firebaseio.com'
})

def referencia(temperatura):
    temperaturaRef = db.reference('componentes/Temperatura')
    temperaturaRef.set(10)
    time.sleep(1)
    temperaturaRef.set(temperatura) #Se manda a Firebase el valor de la Temperatura
    print(temperaturaRef.get())