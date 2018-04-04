import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
# Fetch the service account key JSON file contents
cred = credentials.Certificate('keyAuthorization/domoticaec3882-firebase-adminsdk-rye8h-493394c76b.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://domoticaec3882.firebaseio.com'
})
#Referencias de Firebase
alarmaRef = db.reference('Alarma')
iluminacionRef = db.reference('Iluminacion')
seguridadRef = db.reference('Seguridad')
sismoRef = db.reference('Sismo')
temperaturaRef = db.reference('Temperatura')
ventilacionRef = db.reference('Ventilacion')
valorAnterior = 0

def enviarTemperatura(valorAnterior):
    try:
        f = open('temperatura.txt', 'r')
        temperatura = f.read()
        temperatura = int(temperatura)
        f.close()


        if temperatura is not valorAnterior:
            temperaturaRef.set(temperatura)  # Se manda a Firebase el valor de la Temperatura
            print(temperatura)
            valorAnterior = temperatura
        return valorAnterior

    except:
        f.close()

def enviarNotificacion():
    hola='alarma en cantidades industriales'
    #print(hola)

def procesarSeguridad():
    seguridad = seguridadRef.get()
    try:
        f = open('alarma.txt', 'r')
        alarma = f.read()
        alarma = int(alarma)
        f.close()

        if seguridad is 1 and alarma is 1:
            enviarNotificacion()
    except:
        f.close()

def procesarSismo():
    try:
        f = open('acelerometro.txt', 'r')
        acelerometro = f.read()
        acelerometro = float(acelerometro)
        f.close()
        if acelerometro < 1.4:

    except:
        f.close()
if __name__ == '__main__':
    while True:
       valorAnterior = enviarTemperatura(valorAnterior)
       procesarSeguridad()
       procesarSismo()

