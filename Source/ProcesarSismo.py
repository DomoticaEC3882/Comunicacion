import numpy as np
import time
import math
from subprocess import call

#Constantes
UMBRAL = 1.3
RANGO_SIN_PERTURBACION = 1000



def procesarSismo():
    try:
        f = open('acelerometro.txt', 'r')
        acelerometro = float(f.read())
        f.close()
        if acelerometro < UMBRAL:
            reposo = False
            contadorDeReposo = 0
            captura = []
            tiempoInicial = time.time()
            while reposo is False:
                try:
                    f = open('acelerometro.txt', 'r')
                    acelerometro = float(f.read())
                    f.close()
                    captura = np.append(captura,acelerometro)
                    if acelerometro > UMBRAL:
                        contadorDeReposo = contadorDeReposo + 1
                        if contadorDeReposo > RANGO_SIN_PERTURBACION:
                            tiempoFinal = time.time()
                            print("tiempo final: ", tiempoFinal)
                            calcularMagnitud(tiempoFinal-tiempoInicial,captura)
                            reposo = True
                    else:
                        contadorDeReposo = 0
                except:
                    f.close()
    except:
        f.close()


def calcularMagnitud(tiempo,captura):
    A = 423*(1.43-np.min(captura))             #amplitud maxima del Sismo
    magnitud = round(math.log10(A*(tiempo**3)/1.62),1)
    print("Tiempo del sismo: ",round(tiempo,2))
    print("Maxima amplitud del Sismo: ",round(A,2))
    print("Magnitud del Sismo en escala de Richter: ",magnitud)
    f = open('sismo.txt','w')
    f.write(str(magnitud))
    f.close()
    call("node EnviarNotificacionSismo.js", shell=True)

if __name__ == '__main__':
    while True:
       procesarSismo()