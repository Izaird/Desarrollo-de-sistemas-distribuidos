import socket
import time
from tkinter import *
import tkinter as tk
import threading
import random

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
random.seed(99)
class clockClient:	#Clase Reloj
	def __init__(self, win, _x, _y ):
		self.h = random.randint(0,23)
		self.m = random.randint(0,59)
		self.s = random.randint(0,59)
		self.secTimer = 1 #Valor del sleep para los segundos
		self.status = True
		self.lbl = Label(win,text="%02d:%02d:%02d" % (self.h ,self.m,self.s))
		self.lbl.grid(row = _x , column = _y)
	def start(self , lbl):	#El thread de cada GUIClock llamara a esta funcion
		while(1): #While true para que siempre cheque el status y actualice el reloj
			#print(self.status)
			if(self.status==True):	#Status del reloj, sirve para pausarlo
				sleep(self.secTimer)	#Segun el valor del atributo secTimer es la pausa
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

def RunClient(clk):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while(1):
            time.sleep(1)
            clk.s += 1
            s.sendall(b'Hello, world')
            data = s.recv(32)
            #print( repr(data)  )
            #print("\n", data[2:4])
            minsFromMaster = int(data[2:4])
            #print( data[-2:])
            #print("\n", minsFromMaster)
            if(clk.s  >= 60):
                clk.s = 0
                clk.m += 1
                #print("entre a condicion")
            if(minsFromMaster +1 == 60): #Reset de los minutos si se pasa de 60
                #clk.m = 0
                clk.h += 1
            if(clk.h >= 24):#Reset de las horas si se pasa de 24
                clk.h = 0
            clk.lbl.config(text = "%02d:%02d:%02d" % (clk.h , minsFromMaster, clk.s) )
        s.shutdown(socket.SHUT_RDWR)
        s.close()



win = tk.Tk()
win.geometry("200x100")
#lbl = Label(win , text="%02d" % (0))
clk1 = clockClient(win,0,0)
#lbl.grid(row = 0 , column = 0 , columnspan = 2)
clientThread = threading.Thread(target = RunClient , args = (clk1, ))
clientThread.setDaemon(True)
clientThread.start()
win.mainloop()
