import firebase_admin
import time
import math
from firebase_admin import credentials
from firebase_admin import db
from subprocess import call

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
tokenRef = db.reference('Token')
valorAnterior = 0

#Bandera para el sismo:
f = open('bandera.txt', 'w')
f.write('0')
f.close()

#Tiempo Inicial para el sismo:
f = open('tiempo.txt', 'w')
f.write('0')
f.close()

#Tiempo Acumulado para el sismo:
f = open('tiempoAcumulado.txt', 'w')
f.write('0')
f.close()

#Amplitud Maxima para el sismo:
f = open('amplitud.txt', 'w')
f.write('5')
f.close()

def obtenerToken():
    token = tokenRef.get()
    escribirArchivo('token.txt', token)

def escribirArchivo(nombre,valor):
    f=open(nombre,'w')
    f.write(str(valor))
    f.close()

def leerArchivo(nombre):
    try:
        f=open(nombre,'r')
        valor = f.read()
        f.close()
    except:
        f.close()
    return valor

def leerFirebase():
    iluminacion = iluminacionRef.get()
    ventilacion = ventilacionRef.get()
    escribirArchivo('iluminacion.txt',iluminacion)
    escribirArchivo('ventilacion.txt',ventilacion)



def enviarTemperatura(valorAnterior):
    try:
        f=open('temperatura.txt','r')
        temperatura = int(f.read())
        f.close()
    except:
        temperatura = valorAnterior
        f.close()

    if temperatura is not valorAnterior:
        temperaturaRef.set(temperatura)
        valorAnterior = temperatura
    return valorAnterior

def procesarSeguridad():
    seguridad = seguridadRef.get()
    try:
        f = open('alarma.txt', 'r')
        alarma = f.read()
        alarma = int(alarma)
        f.close()
        if seguridad is 1 and alarma is 1:
            call("node EnviarNotificacionAlarma.js", shell=True)
            seguridadRef.set(0)

    except:
        f.close()

if __name__ == '__main__':
    obtenerToken()
    while True:
       leerFirebase()
       valorAnterior = enviarTemperatura(valorAnterior)
       procesarSeguridad()


