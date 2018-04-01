#Lado del Servidor

import socketserver
import threading
import time
import struct
import comunicacionapp as comapp

class MiTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024) #Me guarda lo que me manda el cliente en data
        data = struct.unpack('!d',data) #Conversión bytes a float (Es una tupla: me interesa solo el primer elemento de la tupla)
        temperatura = data[0]
        comapp.referencia(temperatura)
        time.sleep(0.1) #Espera 0.1 segundos si recibe de vuelta

class ThreadServer(socketserver.ThreadingMixIn,socketserver.TCPServer):  #Nuestro server va a poder abrir un handle por cada cliente que se conecte
    pass

def main():
    host = "localhost"
    port = 9999
    server = ThreadServer((host,port),MiTcpHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print("Server corriendo")

main()