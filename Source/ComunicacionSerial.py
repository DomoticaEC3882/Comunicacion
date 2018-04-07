from subprocess import call
import serial
import numpy as np

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
contador = 0

def leerArchivo(nombre):
    try:
        f=open(nombre,'r')
        valor = f.read()
        f.close()
    except:
        f.close()
    return valor

def leerParametros():
    ##LECTURA DEL PUERTO SERIAL
    mensaje = port.read(1 + 2 * cantidad_canales)
    hall = (mensaje[1] & 64) >> 6  # entrada digital 1
    ultrasonido = (mensaje[1] & 32) >> 5  # entrada digital 2
    for canal in range(0,2):
        analogico[canal] = (((mensaje[1+2*canal] & 31) << 7) + mensaje[2+2*canal])/2**12
    acelerometro = MAX_ACELEROMETRO*analogico[0]
    acelerometro = round(acelerometro,4)

    temperatura = int(MAX_TEMPERATURA*analogico[1])

    #LEER FIREBASE LOCAL
    iluminacion = leerArchivo('iluminacion.txt')
    ventilacion = leerArchivo('ventilacion.txt')

    return acelerometro,temperatura,hall,ultrasonido,iluminacion,ventilacion

def escribirPuerto(iluminacion,ventilacion):
    try:
        seleccion = str(int(iluminacion)+2*int(ventilacion))
        port.write(seleccion.encode())
    except:
        print('leyomal')

def procesarSismo(acelerometro):
    acelerometro = str(acelerometro)
    f = open('acelerometro.txt', 'w')
    f.write(acelerometro)
    f.close()

def procesarTemperatura(temperatura):
    temperatura = str(temperatura)
    f = open('temperatura.txt', 'w')
    f.write(temperatura)
    f.close()

def procesarAlarma(hall, ultrasonido):
    if hall is 0:
        if ultrasonido is 1:
            f = open('alarma.txt', 'w')
            f.write('1')
            f.close()
    else:
        f = open('alarma.txt', 'w')
        f.write('0')
        f.close()

if __name__ == '__main__':
    while True:
        acelerometro, temperatura, hall, ultrasonido,iluminacion,ventilacion = leerParametros()
        print(acelerometro, temperatura, hall, ultrasonido,iluminacion,ventilacion)
        escribirPuerto(iluminacion, ventilacion)
        procesarSismo(acelerometro)
        procesarTemperatura(temperatura)
        procesarAlarma(hall, ultrasonido)