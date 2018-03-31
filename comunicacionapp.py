#comunicacionapp

import firebase_admin
import time
from firebase_admin import credentials
from firebase_admin import db
import math
import numpy as np

# Fetch the service account key JSON file contents
cred = credentials.Certificate('domoticaec3882-firebase-adminsdk-rye8h-493394c76b.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://domoticaec3882.firebaseio.com'
})

def referencia(temperatura):
    temperatura = int(temperatura)
    temperaturaRef = db.reference('Temperatura')
    temperaturaRef.set(temperatura) #Se manda a Firebase el valor de la Temperatura
    print(temperaturaRef.get())

def deteccion(valor):
    alarmaRef = db.reference('Alarma')
    alarmaRef.set(valor) #Se manda la alarma a Firebase


def sismo(acelerometro,tiempo):
    amplitud_maxima = 1.43 - acelerometro #Como el acelerometro siempre muestra 1.43 en la salida y baja dicho valor cuando se mueve. Entonces la amplitud la calculamos de esa manera
    magnitud = math.log((((amplitud_maxima*1000) * (tiempo ** 3)) / 1.62),10)  # Se hace el cálculo en la escala de Richter
    magnitud = round(magnitud,1)
    magnitudRef = db.reference('Sismo')
    magnitudRef.set(magnitud)  # Se manda a Firebase el valor del Sismo
    print(magnitudRef.get())