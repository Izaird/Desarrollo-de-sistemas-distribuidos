import socket, struct, sys, time
from datetime import timedelta

NTP_SERVER1 = ('0.uk.pool.ntp.org','0.mx.pool.ntp.org')
NTP_SERVER2 = '0.mx.pool.ntp.org'
LocalIPs = ['127.0.0.1']
localIP = "127.0.0.1"
# reference time (in seconds since 1900-01-01 00:00:00)
# 1970-01-01 00:00:00
TIME1970 = 2208988800


def time_client(Direcciones, Port=9090):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Cree otro socket UDP pra recibir la respuesta,
    #si no el while True del otro socket seguia enviando datos al mismo puerto
    serv.bind((localIP,9091))
    i=0
    for var in Direcciones:  #Direcciones son las IPs de las que queremos sacar la hora
        tiempos = [None]*len(Direcciones)
        data = bytes("Mandame tu hora","utf-8")
        client.sendto(data, (var, Port))
        data, address = serv.recvfrom(1024)   #Recibimos la respuesta en nuestro socket serv bindeado a otro puerto
        if data: print('Response received from:', address)
        tiempos[i] = data.decode("utf-8") #Decodificamos los bytes recibidos
        i=i+1
    print(str(timedelta(seconds=sum(map(lambda f: int(f[0])*3600 + int(f[1])*60 + int(f[2]), map(lambda f: f.split(':'), tiempos)))/len(tiempos))))
    #Separamos los datos por : los convertimos a segundos y les sacamos el promedio
if __name__ == '__main__':
    time_client(LocalIPs)
