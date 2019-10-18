import socket, struct, sys, time
import datetime
from datetime import timedelta
localIP = "127.0.0.1"
#Este es como el servidor de la hora

def send_time(Port=9090): #Uso el puerto 9090 pero puede especificar otro, a ese puerto se le manda el mensaje que se desea la hora
    serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serv.bind((localIP,Port))
    print("UDP server up and listening")

    while True:
        bytesAddressPair = serv.recvfrom(1024)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        print("Message from Client:{}".format(message))
        print("Client IP Address:{}".format(address))#Que recibimos y de donde
        tiempoActual = datetime.datetime.now()
        timeasString = str(tiempoActual.hour) + ":" +  str(tiempoActual.minute) + ":" + str(tiempoActual.second)
        #Mandamos la hora en forma de Horas:Minutos:Segundos
        print(timeasString)#imprimemos la cadena para saber que mandamos
        hour = bytes(timeasString,"utf-8")#Comvertimos la cadena  a bytes
        serv.sendto(hour, (localIP, 9091))#Mandamos la informacion al localhost a otro puerto, porque si no el while True seguira enviando la hora 

if __name__ == '__main__':
    send_time()
    #sntp_client(NTP_SERVER2
