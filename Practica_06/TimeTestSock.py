import threading
import socket

#Script para probar comportamineto del server al mandarle ciertos mensajes
#Este es para mensajes de tiempo
LOCALHOST = '127.0.0.1'
#IPTested = str(input("Direccion a la que deseas hacer pruebas"))
#obtenemos la ip donde esta corriendo el programa para no tener que ingresarla manualmente
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IPTested = s.getsockname()[0]
PORT = 65432        # Puerto de jugador, para enviar y recibir la lista de numeros
BCKPORT = 65433        # Puerto para sincronizacion de BDD entre servidores
TIMEPORT = 60900    #Puerto de sincronizacion de reloj
ELECPORT = 30400   #Puerto de Elecciones

sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM) #Creacion de socket UDP para pruebas
sock.bind((LOCALHOST,TIMEPORT))
sock.settimeout(6)

while True:
    #msg=str(input("Mensaje a enviar"))
    #sock.sendto(msg.encode('utf-8'),(IPTested,ELECPORT))
    try:
        data , addr = sock.recvfrom(100)
        cmdArgs = data.decode('utf-8').split()
        print(cmdArgs)
        if(cmdArgs[0] == "GTM"): #si llega este mensaje
            #msg = str(clk1.clk.getTimeToNumber())#Mandar hora
            msg = "CTM 43665"
            sock.sendto(msg.encode('utf-8'),(addr))
        elif(cmdArgs[0] == "CTM"):#Si llega este mensaje
            print("Hora recibida  ",cmdArgs[1] )
            #clk1.clk.setTimeFromNumber(int(cmdArgs[1]))#Ajustar reloj
    except socket.timeout as e:
        print("Timeout in listentime")
        continue
    except IndexError:
        print("No data received")
        continue
