import threading
import socket

#Script para probar comportamineto del server al mandarle ciertos mensajes
LOCALHOST = '127.0.0.1'
#IPTested = str(input("Direccion a la que deseas hacer pruebas"))
IPTested = '10.100.74.22'
PORT = 65432        # Puerto de jugador, para enviar y recibir la lista de numeros
BCKPORT = 65433        # Puerto para sincronizacion de BDD entre servidores
TIMEPORT = 60900    #Puerto de sincronizacion de reloj
ELECPORT = 30400   #Puerto de Elecciones

sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM) #Creacion de socket UDP para pruebas
sock.bind((LOCALHOST,ELECPORT))
sock.settimeout(2)

while True:
    msg=str(input("Mensaje a enviar"))
    sock.sendto(msg.encode('utf-8'),(IPTested,ELECPORT))
    try:
        data , addr = sock.recvfrom(100)
        print("Respuesta:")
        print(data.decode('utf-8'))
        print("Remitente: ")
        print(addr)
        if (data == "OK"):
            msg="OK"
    except socket.timeout as e:
        print("Socket timeout")
        continue
    except socket.error as err:
        print(err)
