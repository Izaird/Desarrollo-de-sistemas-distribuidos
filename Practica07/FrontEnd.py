import socket
from time import sleep

class Front:
    
    def __init__(self):
        self.IPCordinador = "-1"
        self.HostName = "192.168.0.4"
        self.HostCordPort = 60430
        self.HostServPort = 65432
    

    def getCordinador(self):
        sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        sock.sendto(b'GMC' , (self.HostName , self.HostCordPort))
        data , addr = sock.recvfrom(100)
        self.IPCordinador = data.decode('utf-8')
        print("IP del cordinador: %s" % self.IPCordinador)

    def sendListOfNumbers(self, file2open):
         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.IPCordinador, self.HostServPort))
            #time.sleep(0.001)
            archivo = open(file2open, "rb")
            print("Enviando...")
            l = archivo.read(1024)
            while (l):
                print("Enviando...")
                s.send(l)
                l = archivo.read(1024)
            print("Envio Completado")
            print (s.recv(1024))
            s.shutdown(socket.SHUT_WR)
            s.close

            sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
            sock.sendto(b'SNA' , (self.IPCordinador , self.HostCordPort))
            sleep(0.5)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.IPCordinador, self.HostCordPort-3))
                #time.sleep(0.001)
                archivo.seek(0)
                print("Enviando...")
                l = archivo.read(1024)
                while (l):
                    print("Enviando...")
                    s.send(l)
                    l = archivo.read(1024)
                archivo.close()
                print("Envio Completado")
                print (s.recv(1024))
                s.shutdown(socket.SHUT_WR)
                s.close