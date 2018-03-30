import firebase_admin
import time
from firebase_admin import credentials
from firebase_admin import db
import math

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

def sismo(acelerometro):
    tiempo_inicial = time.time() #Se establece el tiempo inicial para empezar a contar en segundos
    amplitud_inicial = 1.5 - acelerometro #Como el acelerometro siempre muestra 1.5 en la salida y baja dicho valor cuando se mueve. Entonces la amplitud la calculamos de esa manera
    while(acelerometro <= 1.45): #Se establece un ciclo infinito hasta que el sismo pase
       if(acelerometro <= amplitud_inicial):
            amplitud_maxima = 1.5 - acelerometro
    tiempo_final = time.time() - tiempo_inicial  # Se establece el tiempo final restando el tiempo actual menos el tiempo inicial (segundos)
    tiempo_final_entero = int(tiempo_final)
    magnitud = math.log((((amplitud_maxima*1000) * (tiempo_final_entero ** 3)) / 1.62),10)  # Se hace el cálculo en la escala de Richter
    magnitud = int(magnitud)
    magnitudRef = db.reference('Sismo')
    magnitudRef.set(magnitud)  # Se manda a Firebase el valor del Sismo
    print(magnitudRef.get())