import numpy as np
import serial
import comunicacionapp as comapp

#Constantes
MAX_ACELEROMETRO = 3
MAX_TEMPERATURA = 50
BANDERA_SISMO = 1.4

#Parametros para el puerto serial
nombre_puerto = 'COM3'
baudios = 115200
timeout = 1
cantidad_canales = 2

#inicializar puerto comunicacion serial
port = serial.Serial(nombre_puerto, baudios, timeout = timeout)

#inicializar variable para recibir data
analogico = [0,0]
eventoSismo = np.zeros(0)

def procesarAlarma(hall,ultrasonido):
    if hall is 1:
        if ultrasonido is 1:
            comapp.deteccion(hall) ##aprovecho que hall ya vale 1


def procesarSismografo(acelerometro):
    if(acelerometro < BANDERA_SISMO):
        hola =acelerometro

def procesarTemperatura(temperatura):
    comapp.referencia(temperatura)


def leerPuerto():
    ##LECTURA DEL PUERTO
    mensaje = port.read(1 + 2 * cantidad_canales)
    hall = (mensaje[1] & 64) >> 6  # entrada digital 1
    ultrasonido = (mensaje[1] & 32) >> 5  # entrada digital 2
    ultrasonido = 1
    for canal in range(0,2):
        analogico[canal] = (((mensaje[1+2*canal] & 31) << 7) + mensaje[2+2*canal])/2**12
    acelerometro = MAX_ACELEROMETRO*analogico[0]
    temperatura  = MAX_TEMPERATURA*analogico[1]

    return acelerometro,temperatura,hall,ultrasonido

if __name__ == '__main__':
    while True:
        acelerometro,temperatura,hall,ultrasonido = leerPuerto()
        print(acelerometro,temperatura,hall,ultrasonido)
        ##ANALISIS EN TIEMPO REAL
        # Sismografo
        procesarSismografo(acelerometro)
        # Temperatura
        procesarTemperatura(temperatura)
        # Alarma
        procesarAlarma(hall, ultrasonido)
