# from tkinter import *
from tkinter import Label, Button, Toplevel, Entry
import tkinter as tk
from datetime import datetime
import random
from time import sleep
import threading
import socket
import mysql.connector
from getpass import getpass

def toTime(num):
        cadena = ""
        cadena += str(num//10000)+":"
        num -= (num//10000)*10000
        cadena += str(num//100)+":"
        num -= (num//100)*100
        cadena += str(num)
        return cadena

def makeAjust(sock):
        prom = 0 
        global listOfServers
        if(len(listOfServers) > 0):
                for x in listOfServers:
                        print("[%s , %d]" % (x , TIMEPORT) )
                        sock.sendto(b'GTM',(x,TIMEPORT))
                        data , addr = sock.recvfrom(100)
                        prom += int(data.decode('utf-8'))
                        print(prom)
                prom = prom // len(listOfServers)
                MSG = "CTM " + str(prom)
                hora = toTime(prom)
                sqlformula = "INSERT INTO Tiempo (hora) VALUES(\"%s\")"
                mycursor_time.execute(sqlformula,(hora,))
                mydb_time.commit()
                for x in listOfServers:
                #       print(()x , TIMEPORT)
                        sock.sendto(MSG.encode('utf-8'),(x,PORT))

class clock:    #Clase Reloj
    def __init__(self , isRandom):
        if isRandom:
            self.h = random.randint(0,23)
            self.m = random.randint(0,59)
            self.s = random.randint(0,59)
            self.secTimer = 1
        else:
            self.h = int(now.strftime("%H"))
            self.m = int(now.strftime("%M"))
            self.s = int(now.strftime("%S"))
            self.secTimer = 1 #Valor del sleep para los segundos
        self.status = True
    def start(self , lbl):      #El thread de cada GUIClock llamara a esta funcion
        while(1): #While true para que siempre cheque el status y actualice el reloj
            #print(self.status)
            if(self.status==True):      #Status del reloj, sirve para pausarlo
                sleep(self.secTimer)    #Segun el valor del atributo secTimer es la pausa
                self.s += 1
                if(self.s >= 60 ): #Reset de los segundos si se pasa de 60
                    self.s = 0
                    self.m += 1
                if(self.m >= 60): #Reset de los minutos si se pasa de 60
                    self.m = 0
                    self.h += 1
                if(self.h >= 24):#Reset de las horas si se pasa de 24
                    self.h = 0
                lbl.config(text = "%02d:%02d:%02d" % (self.h , self.m , self.s))
            else:
                sleep(1)
    def pauseClock(self):
        self.status=False
    def resumeClock(self):
        self.status=True
    def getTimeToNumber(self):
        return self.h*10000+self.m*100+self.s
    def setTimeFromNumber(self,num):
        x = self.getTimeToNumber()
        if x <= num:
            self.h = num//10000
            num -= self.h*10000
            self.m = num//100
            num -= self.m*100
            self.s = num
        else:
            x -= num
            self.secTimer = 0.5
            sleep(2*x)
            self.secTimer = 1

class GUIClock:         #La GUI del reloj estara definida en esta clase
    def __init__(self, win, _x , _y): #win es la ventana en la cual colocaremos el reloj, _x y _y es la posicionamiento tipo grid
        self.clk = clock(True) #Creamos un atributo del tipo clock
        #win.title("Window")
        self.total = 0
        self.lbl = Label(win, text="%02d:%02d:%02d" % (self.clk.h , self.clk.m , self.clk.s))
        self.lbl.grid(row = _x , column = _y, columnspan=2)
        self.lbltotal= Label(win, text="La suma de los elementos recibidos es: %d" %(self.total))
        self.lbltotal.grid(row=_x+1, column=_y, columnspan=2)
        self.btn = Button(win, text ="Modificar horas", command = lambda: self.popup_clock_config(win, 0)  )
        self.btn.grid(row = _x+2, column = _y)
        self.btn = Button(win, text ="Modificar minutos", command = lambda: self.popup_clock_config(win, 1)  )
        self.btn.grid(row = _x+3, column = _y)
        self.btn = Button(win, text ="Modificar segundos", command = lambda: self.popup_clock_config(win, 2)  )
        self.btn.grid(row = _x+4, column = _y)
        self.btn = Button(win, text ="configurar segundero", command =lambda: self.popup_clock_config(win, 3)  )
        self.btn.grid(row = _x+5, column = _y)
        self.t = threading.Thread(target=self.clk.start , args=(self.lbl, ))
        self.t.setDaemon(True)
        self.t.start()
    def setTimeGUI(self,horas, minutos, segundos): #Funcion que establece los valore del reloj
        self.clk.h = int(horas)
        self.clk.m = int(minutos)
        self.clk.s = int(segundos)
        self.clk.status=True
        self.lbl.config(text = "%02d:%02d:%02d" % (self.clk.h , self.clk.m , self.clk.s))
    def setTimeGUI_By_Selection(self,win,value,type): #Funcion que establece los valore del reloj
        if len(value) > 0:
            if(type == "s"):
                self.clk.s = int(value) % 60
            elif(type == "m"):
                self.clk.m = int(value) % 60
            elif(type == "h"):
                self.clk.h = int(value) % 24
            else:
                self.clk.secTimer = float(value)
            self.clk.status=True
            self.lbl.config(text = "%02d:%02d:%02d" % (self.clk.h , self.clk.m , self.clk.s))
            win.destroy()
    def popup_clock_config(self,win, ElemAModificar):#Funcion para la modificacion de los valores del reloj con GUI
        self.clk.status=False   #Paramos el reloj
        #ven = Toplevel()       #Creamos un ventana pop up
        ven = Toplevel()
        ven.protocol("WM_DELETE_WINDOW", lambda window=ven : self.onCloseWindow(window))
        entrada=Entry(ven)
        entrada.grid(row=1, column=1)
        if ElemAModificar == 0:                         # 0 indica que actua sobre horas
            label1 = Label(ven, text = 'Modificar Horas') #Colocamos labels y entries en la ventana pop up
            label1.grid(row=0, column=0, columnspan=2)
            labelHoras = Label(ven, text = 'Introduce las horas')
            labelHoras.grid(row=1, column=0)
            b1 = Button(ven, text= "Cambiar horas", command= lambda: GUIClock.setTimeGUI_By_Selection(self,ven,entrada.get(),"h") )
            b1.grid(row=2, column=0)
        elif ElemAModificar == 1:       # 1 indica que actua sobre minutos
            label1 = Label(ven, text = 'Modificar Minutos')
            label1.grid(row=0, column=0, columnspan=2)
            labelminutos = Label(ven, text = 'Introduce los minutos que deseas')
            labelminutos.grid(row=1, column=0)
            b1 = Button(ven, text= "Cambiar Minutos", command= lambda: GUIClock.setTimeGUI_By_Selection(self,ven,entrada.get(),"m") )
            b1.grid(row=2, column=0)
        elif ElemAModificar == 2:               # 2 indica que actua sobre segundos
            label1 = Label(ven, text = 'Modificar segundos')
            label1.grid(row=0, column=0, columnspan=2)
            labelSeg = Label(ven, text = 'Introduce los segundos que deseas')
            labelSeg.grid(row=1, column=0)
            b1 = Button(ven, text= "Cambiar Segundos", command= lambda: GUIClock.setTimeGUI_By_Selection(self,ven,entrada.get(),"s") )
            b1.grid(row=2, column=0)
        elif ElemAModificar == 3:
            label1 = Label(ven, text = 'Modificar segundero')
            label1.grid(row=0, column=0, columnspan=2)
            labelSeg = Label(ven, text = 'Introduce cada cuanto se actualizara el segundero del reloj')
            labelSeg.grid(row=1, column=0)
            b1 = Button(ven, text= "Cambiar Segundos", command= lambda: GUIClock.setTimeGUI_By_Selection(self,ven,entrada.get(),"t") )
            b1.grid(row=2, column=0)
    def onCloseWindow(self , window):
        self.clk.status = True
        window.destroy()

class Comunicator:
    def __init__(self, clk1, IPBackUp):
        self.backupEnable = False
        self.addr = ""
        RunListenThread = threading.Thread(target=self.RunSocket , args=(clk1 , ))
        listenBCKThread = threading.Thread(target=self.listenBackUp , args=(clk1, ))
        turnOnBackUpThread = threading.Thread(target=self.turnOnBackUp , args=(IPBackUp,))
        RunListenThread.setDaemon(True)
        turnOnBackUpThread.setDaemon(True)
        listenBCKThread.setDaemon(True)
        RunListenThread.start()
        listenBCKThread.start()
        turnOnBackUpThread.start()
        listenTimeThread = threading.Thread(target=self.listenTime , args=(clk1,))
        listenTimeThread.setDaemon(True)
        listenTimeThread.start()

    def turnOnBackUp(self, IPBackUp):

        if (IPBackUp != ""):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                try:
                    s.sendto(b"ACKB",(IPBackUp,BCKPORT))
                    data , self.addr = s.recvfrom(4)
                    if(repr(data)[2:-1] == "ACKB"):
                        self.backupEnable = True
                        s.sendto(b"ACKC" , (HOST , BCKPORT))
                except EnvironmentError as e:
                    pass
                
        sleep(0.01)

    def listenBackUp(self, clk1):
        global BKHOST
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((HOST , BCKPORT))
            while not self.backupEnable:
                data , self.addr = s.recvfrom(4)
                if(repr(data)[2:-1] == "ACKB"):
                    self.backupEnable = True
                    s.sendto(b"ACKB" , self.addr)
                    BKHOST = self.addr[0]
        self.listenServer(clk1)

    def listenServer(self, clk1):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((HOST , BCKPORT))
            while self.backupEnable:
                data , x = s.recvfrom(1024)
                args = data.decode('utf-8').split()
                self.executeSQLInsert(args[0] , args[1] , args[2] , clk1)

    def RunSocket(self,GUIclk):
        totalData=0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #Creamos el socket le ponemos el nombre de s, AF_INET=IPV4 SOCK_STREAM=TCP
            s.bind((HOST, PORT))#Publicamos la ip y puerto
            s.listen(4)#Aceptaremos maximo 4 conexiones
            while True:#Loop infinito para siempre estar escucahndo al puerto especificado
                conn, addr = s.accept() #Aceptar la conexion
                print(f"Conection desde {addr} ha sido establecida")
                conn.send(bytes("Conectado a servidor", "utf-8"))
                totalData=0
                l = conn.recv(1024)
                while (l): #Mientras l reciva algo entrara en este loop
                    print("Recibiendo...")
                    print(l)    #Recibiremos una cadena de bytes
                    #print (type(l))
                    listofData=l.split(b'\n') #Separamos la cadena de bytes por breaklines
                    print(listofData)#l ahora es una lista con cadenas de bytes
                    for i in range(0, len(listofData)):
                        if ( listofData[i].decode("utf-8")=='' ):
                            listofData[i]=0
                        else:
                            listofData[i] = int(listofData[i].decode("utf-8") ) #se decodifica y castea a entero
                        totalData = listofData[i]+totalData
                        print(totalData)
                    print(listofData)
                    l = conn.recv(1024)
                print("Termine de recibir")
                conn.send(b'Envio Completado')
                conn.close()
                GUIclk.total = totalData
                hour = str(GUIclk.clk.h).zfill(2) + ":" +str(GUIclk.clk.m).zfill(2)+ ":" +str(GUIclk.clk.s).zfill(2)
                ip = addr[0]

                self.executeSQLInsert(str(totalData) , ip , hour , GUIclk)
                if(self.backupEnable):
                    MGS = str(totalData) + " " + str(ip) + " " + str(hour)
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                        print(BKHOST)
                        sock.sendto(MGS.encode('utf-8') , (BKHOST , BCKPORT))

    def executeSQLInsert(self , totalData , ip , hour , GUIclk):
        outcome =  (totalData, ip, hour)
        mycursor.execute(sqlformula,outcome)
        mydb.commit()
        GUIclk.lbltotal.config(text = "La suma de los elementos recibidos %d" %int(totalData))

    def listenTime(self , clk1):
        sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        sock.bind((HOST , TIMEPORT))
        while True:
            data , addr = sock.recvfrom(100)
            cmdArgs = data.decode('utf-8').split()
            if(cmdArgs[0] == "GTM"):
                msg = str(clk1.clk.getTimeToNumber())
                sock.sendto(msg.encode('utf-8'),(addr))
            elif(cmdArgs[0] == "CTM"):
                clk1.clk.setTimeFromNumber(int(cmdArgs[1]))

#obtenemos la ip donde esta corriendo el programa para no tener que ingresarla manualmente 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
print(HOST)
s.close()
#Se pide la contrasenia de la base de datos
password = getpass("Introduzca su contraseña:")
#Coneccion a la base de datos y uso de Central
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="Central"
)
mycursor = mydb.cursor()
sqlformula = "INSERT INTO Sumas (resultado, ip, hora) VALUES(%s,%s,%s)"

#Coneccion a la base de datos y uso de Time 
mydb_time = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="Tiempo"
)
mycursor_time = mydb_time.cursor()

#lista de las direcciones Ip de los servidores
listOfServers = [HOST,"192.168.100.28"]


BKHOST = "192.168.43."
#Puerto 
PORT = 62000        # Port to listen on (non-privileged ports are > 1023)
BCKPORT = 62001        # Port to listen on (non-privileged ports are > 1023)
TIMEPORT = 62002
now = datetime.now() # Fecha y hora actuales
random.seed(99)


sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
sock.bind((HOST,PORT))

win = tk.Tk()
win.geometry("800x600") #Tamaño de la aplicación
#win.resizable(1,1)     #Esto permite a la app adaptarse al tamaño
clk1 = GUIClock(win,0,0)        #iniciamos el reloj maestro en la posicion 0, 0
com = Comunicator(clk1,BKHOST)

win.mainloop()