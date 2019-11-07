from tkinter import *
import tkinter as tk
from datetime import datetime
import random
from time import sleep
import threading
import socket
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


now = datetime.now() # Fecha y hora actuales
random.seed(99)
class clock:	#Clase Reloj
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


class GUIClock:		#La GUI del reloj estara definida en esta clase
	def __init__(self, win, _x , _y): #win es la ventana en la cual colocaremos el reloj, _x y _y es la posicionamiento tipo grid
		self.clk = clock(True) #Creamos un atributo del tipo clock
		#win.title("Window")
		self.lbl = Label(win, text="%02d:%02d:%02d" % (self.clk.h , self.clk.m , self.clk.s))
		self.lbl.grid(row = _x , column = _y, columnspan=2)
		self.btn = Button(win, text ="Modificar horas", command = lambda: self.popup_clock_config(win, 0)  )
		self.btn.grid(row = _x+1, column = _y)
		self.btn = Button(win, text ="Enviar horas", command = lambda: self.popup_clock_config(win, 0)  )
		self.btn.grid(row = _x+1, column = _y+1)
		self.btn = Button(win, text ="Modificar minutos", command = lambda: self.popup_clock_config(win, 1)  )
		self.btn.grid(row = _x+2, column = _y)
		self.btn = Button(win, text ="Enviar minutos", command = lambda: self.popup_clock_config(win, 1)  )
		self.btn.grid(row = _x+2, column = _y+1)
		self.btn = Button(win, text ="Modificar segundos", command = lambda: self.popup_clock_config(win, 2)  )
		self.btn.grid(row = _x+3, column = _y)
		self.btn = Button(win, text ="Enviar segundos", command = lambda: self.popup_clock_config(win, 2)  )
		self.btn.grid(row = _x+3, column = _y+1)
		self.btn = Button(win, text ="configurar segundero", command =lambda: self.popup_clock_config(win, 3)  )
		self.btn.grid(row = _x+4, column = _y)
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
				self.clk.s = int(value)	% 60
			elif(type == "m"):
				self.clk.m = int(value)	% 60
			elif(type == "h"):
				self.clk.h = int(value) % 24
			else:
				self.clk.secTimer = float(value)
			self.clk.status=True
			self.lbl.config(text = "%02d:%02d:%02d" % (self.clk.h , self.clk.m , self.clk.s))
			win.destroy()
	def popup_clock_config(self,win, ElemAModificar):#Funcion para la modificacion de los valores del reloj con GUI
		self.clk.status=False	#Paramos el reloj
		#ven = Toplevel()	#Creamos un ventana pop up
		ven = Toplevel()
		ven.protocol("WM_DELETE_WINDOW", lambda window=ven : self.onCloseWindow(window))#Sobreescribimos el comportamiento al cerrar el popup
		entrada=Entry(ven)
		entrada.grid(row=1, column=1)
		if ElemAModificar == 0:
			label1 = Label(ven, text = 'Modificar Horas') #Colocamos labels y entries en la ventana pop up
			label1.grid(row=0, column=0, columnspan=2)
			labelHoras = Label(ven, text = 'Introduce las horas')
			labelHoras.grid(row=1, column=0)
			b1 = Button(ven, text= "Cambiar horas", command= lambda: GUIClock.setTimeGUI_By_Selection(self,ven,entrada.get(),"h") )
			b1.grid(row=2, column=0)
		elif ElemAModificar == 1:
			label1 = Label(ven, text = 'Modificar Minutos')
			label1.grid(row=0, column=0, columnspan=2)
			labelminutos = Label(ven, text = 'Introduce los minutos que deseas')
			labelminutos.grid(row=1, column=0)
			b1 = Button(ven, text= "Cambiar Minutos", command= lambda: GUIClock.setTimeGUI_By_Selection(self,ven,entrada.get(),"m") )
			b1.grid(row=2, column=0)
		elif ElemAModificar == 2:
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
			#Timer = float_bin(int(entrada.get), 6)
			b1 = Button(ven, text= "Cambiar Segundos", command= lambda: GUIClock.setTimeGUI_By_Selection(self,ven,entrada.get(),"t") )
			b1.grid(row=2, column=0)

	def onCloseWindow(self , window):
		self.clk.status = True
		window.destroy()

def RunSocket(GUIclk):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		while(1):
			conn, addr = s.accept()
			with conn:
				while(1):
					query = conn.recv(1024)
					if not query:
						break
					conn.sendall(b'%02d%02d%02d' % (GUIclk.clk.h , GUIclk.clk.m, GUIclk.clk.s)) #
				print(b'%02d:%02d:%02d' % (GUIclk.clk.h , GUIclk.clk.m, GUIclk.clk.s))
				print("AA")


win = tk.Tk()

win.geometry("530x200") #Tamaño de la aplicación
#win.resizable(1,1)	#Esto permite a la app adaptarse al tamaño
clk1 = GUIClock(win,0,0)	#iniciamos el reloj maestro en la posicion 0, 0
ServerThread = threading.Thread(target=RunSocket , args=(clk1 , ))
ServerThread.setDaemon(True)
ServerThread.start()
win.mainloop()
