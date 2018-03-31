#ComunicacionSerial


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import AnalisisSeñales as ans
import serial
import threading
import time
import comunicacionapp as comapp

#Constantes
MAX_ACELEROMETRO = 3
MAX_TEMPERATURA = 50

#Parametros para el puerto serial
nombre_puerto = 'COM3'
baudios = 115200
timeout = 1
cantidad_canales = 2
espera = 1

port = serial.Serial(nombre_puerto, baudios, timeout = timeout)

limiteRepeticion = 50

analogico = [0,0]

fig = plt.figure()

ax1 = fig.add_subplot(2,1,1)
linea1 = ax1.plot([],[])
ax1.set_ylim([0, 3])
ax1.set_xlim([0, limiteRepeticion])

ax2 = fig.add_subplot(2,1,2)
linea2 = ax2.plot([],[],color='red')
ax2.set_ylim([0, 50])
ax2.set_xlim([0, limiteRepeticion])

lineas = [linea1[0], linea2[0]]

xdata1 = []
xdata2 = []
ydata1 = []
ydata2 = []

bandera = 0

def leerPuerto():
    mensaje = port.read(1 + 2 * cantidad_canales)
    digital1 = (mensaje[1] & 64) >> 6  # entrada digital 1
    digital2 = (mensaje[1] & 32) >> 5  # entrada digital 2
    digital2 = 1 #Mientras tanto porque no tenemos el Sensor de Ultrasonido
    if(digital1==0 and digital2==1):
        valor = 1
        comapp.deteccion(valor)

    #print(digital1," ",digital2)
    for canal in range(0,2):
        analogico[canal] = (((mensaje[1+2*canal] & 31) << 7) + mensaje[2+2*canal])/2**12
    sismo = MAX_ACELEROMETRO * analogico[0]
    temperatura = MAX_TEMPERATURA * analogico[1]
    print(sismo, " ", temperatura)

    comapp.referencia(temperatura) #Se manda el valor de la Temperatura a la funcion referencia de comunicacionapp.py
    threading.Timer(1/10000.,leerPuerto).start()
    return sismo

def escribirPuerto():
    while 1:

        c = '1'
        port.write(c.encode())

def next():
    i = 0
    while True:
        i += 1
        yield i
def update(i):
    y = MAX_ACELEROMETRO * analogico[0]
    # if(y<=1.3): #Condicional para que se procese la medida del sismo
    #     comapp.sismo(y)
    ydata1.append(y)
    xdata1.append(i)
    lineas[0].set_data(xdata1, ydata1)

    y = MAX_TEMPERATURA * analogico[1]
    # comapp.referencia(y) #Se manda el valor de la Temperatura a la funcion referencia de comunicacionapp.py
    #Graficación de la señal de Temperatura:
    ydata2.append(y)
    xdata2.append(i)
    lineas[1].set_data(xdata2, ydata2)
    if i > limiteRepeticion:
        ax1.set_xlim(i - limiteRepeticion, i)
        ax2.set_xlim(i - limiteRepeticion, i)
    else:
        ax1.set_xlim(0, limiteRepeticion)
        ax2.set_xlim(0, limiteRepeticion)
    return lineas

if __name__ == '__main__':
    a = animation.FuncAnimation(fig, update, next, blit = True, interval = 60,
                               repeat = False)
    sismo = leerPuerto()

    if(sismo <= 1.4 and bandera == 0):  # Condicional para que se procese la medida del sismo. bandera == 0 significa que no habia un sismo antes
        valores_acelerometro = np.zeros((0, 1))  # Se inicializa vacio el arreglo de los valores_acelerometro
        tiempo_inicial = time.time()  # Se establece el tiempo inicial para empezar a contar en segundos
        valores_acelerometro = np.vstack([valores_acelerometro,sismo])
        bandera = 1

    if(sismo <= 1.4 and bandera == 1): #Continúa el sismo (bandera = 1). Por lo tanto, se sigue almacenando el valor del sismo
        valores_acelerometro = np.vstack([valores_acelerometro,sismo])

    if(sismo > 1.4 and bandera == 1): #Paró el sismo. Se hace bandera = 0
        tiempo_final = time.time() - tiempo_inicial  # Se establece el tiempo final restando el tiempo actual menos el tiempo inicial (segundos)
        tiempo_final_entero = int(tiempo_final)
        amplitud_sismo = valores_acelerometro.min()
        bandera = 0
        comapp.sismo(amplitud_sismo,tiempo_final_entero)  # Se manda el valor del Sismo a la función sismo de comunicacionapp.py

    escribirPuerto()
    plt.show()
    _, y =np.asarray(linea1.get_data())
    ans.analisis(y)