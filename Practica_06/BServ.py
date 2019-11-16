from tkinter import *
import tkinter as tk
from datetime import datetime
import random
from time import sleep
import threading
import socket
import mysql.connector

#obtenemos la ip donde esta corriendo el programa para no tener que ingresarla manualmente 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
print(HOST)
#HOST = '127.0.0.1'   Standard loopback interface address (localhost)
BKHOST = "10.100.76.183"
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
BCKPORT = 65433        # Port to listen on (non-privileged ports are > 1023)
TIMEPORT = 60900
ELECPORT = 30400
now = datetime.now() # Fecha y hora actuales
random.seed(99)

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="root1234",
	database="Central"
)
mycursor = mydb.cursor()
sqlformula = "INSERT INTO Sumas (resultado, ip, hora) VALUES(%s,%s,%s)"

listOfServers = ['192.168.0.15']
listServswithPrio = [ ['10.100.76.183', 5], ['10.100.68.151', 10],['127.0.0.1', 1]]
listServswithPrio=sorted(listServswithPrio, key= lambda x: x[1], reverse= True)#Ordenar lista por prioridad
print("Lista de servidores ordenados por prioridad: ")
print(listServswithPrio)

def toTime(num):
	cadena = ""
	cadena += str(num//10000)+":"
	num -= (num//10000)*10000
	cadena += str(num//100)+":"
	num -= (num//100)*100
	cadena += str(num)
	return cadena

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
		while(1): #While True para que siempre cheque el status y actualice el reloj
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


class GUIClock:		#La GUI del reloj estara definida en esta clase
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
		ven.protocol("WM_DELETE_WINDOW", lambda window=ven : self.onCloseWindow(window))
		entrada=Entry(ven)
		entrada.grid(row=1, column=1)
		if ElemAModificar == 0:				# 0 indica que actua sobre horas
			label1 = Label(ven, text = 'Modificar Horas') #Colocamos labels y entries en la ventana pop up
			label1.grid(row=0, column=0, columnspan=2)
			labelHoras = Label(ven, text = 'Introduce las horas')
			labelHoras.grid(row=1, column=0)
			b1 = Button(ven, text= "Cambiar horas", command= lambda: GUIClock.setTimeGUI_By_Selection(self,ven,entrada.get(),"h") )
			b1.grid(row=2, column=0)
		elif ElemAModificar == 1:	# 1 indica que actua sobre minutos
			label1 = Label(ven, text = 'Modificar Minutos')
			label1.grid(row=0, column=0, columnspan=2)
			labelminutos = Label(ven, text = 'Introduce los minutos que deseas')
			labelminutos.grid(row=1, column=0)
			b1 = Button(ven, text= "Cambiar Minutos", command= lambda: GUIClock.setTimeGUI_By_Selection(self,ven,entrada.get(),"m") )
			b1.grid(row=2, column=0)
		elif ElemAModificar == 2:		# 2 indica que actua sobre segundos
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
	def __init__(self , clk1 , IPBackUp):
		self.backupEnable = False
		self.MasterStatus = False
		self.ElectionStatus = False  #Election satus sera una bandera False para no hay eleccion True para indicar que esta en proceso
		self.addr = ""
		self.prioridad= 10    #A mayor prio, mas preferente para ser coordinador de tiempo
		self.prioCount = 0	#Contador para saber si recibimos respuesta de un server con mayor prioridad
		self.RunListenThread = threading.Thread(target=self.RunSocket , args=(clk1 , ))
		self.listenBCKThread = threading.Thread(target=self.listenBackUp , args=(clk1, ))
		self.turnOnBackUpThread = threading.Thread(target=self.turnOnBackUp , args=(IPBackUp,))
		self.RunElectionThread = threading.Thread(target=self.ElectionSock , args=(IPBackUp,))#Socket/hilo para los procesos de eleccion de cooridinador
		self.RunElectionThread.setDaemon(True)
		self.listenTimeThread = threading.Thread(target=self.listenTime , args=(clk1,))#sincronizacion de reloj
		self.listenTimeThread.setDaemon(True)
		self.listenTimeThread.start()
		self.RunListenThread.setDaemon(True)
		self.turnOnBackUpThread.setDaemon(True)
		self.listenBCKThread.setDaemon(True)
		self.RunElectionThread.start()
		self.RunListenThread.start()# manejador de jugadores
		self.listenBCKThread.start()
		self.turnOnBackUpThread.start()
	
	def makeAjust(self, sock, clk1):
		prom = 0
		global listServswithPrio
		TMSG=""
		if( self.MasterStatus == True ):
			print("Empezando Consulta")
			for x in range(0,len(listServswithPrio)):
				if (HOST != listServswithPrio[x][0]):
					print("[%s , %d]" % (listServswithPrio[x][0] , PORT) )
					print("Pidiendo hora")
					sock.sendto(b'GTM',(listServswithPrio[x][0],PORT))
					try:
						data , addr = sock.recvfrom(100)
						prom += int(data.decode('utf-8'))
						print(prom)
					except socket.timeout as e:
						#print(e)
						prom += int( clk1.clk.getTimeToNumber())
						continue
					prom = prom // len(listOfServers)
					print("Promedio del tiempo = ",prom)
					TMSG = "CTM " + str(prom)
					hora = toTime(prom)
					"""sqlformula = "INSERT INTO Tiempo (hora) VALUES(\"%s\")"
					mycursor.execute(sqlformula,(hora,))
					mydb.commit()"""
			for j in range(0,len(listServswithPrio)):
				if (HOST != listServswithPrio[x][0] ):
					print("Mandando ajuste a: "+listServswithPrio[j][0])
					print("Promedio    ", prom)
					sock.sendto(TMSG.encode('utf-8'),(listServswithPrio[j][0],PORT))

	def ElectionSock(self,IPBackUp):
		global listOfServers
		global listServswithPrio
		#listServswithPrio=sorted(listServswithPrio, key= lambda x: x[1], reverse= True)#Ordenar lista por prioridad
		#print(listServswithPrio)
		sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
		sock.bind((HOST , ELECPORT))
		sock.settimeout(4)
		while True:
			if(self.MasterStatus == True and self.ElectionStatus == False):#Si somos coordinador de tiempo mandamos pulsos a todos
				print("Soy Coordinador")
				sock.settimeout(2)#Si no responden en 2 s, no nos importa, continuamos mandando pulsos a los demas
				for x in range(0,len(listServswithPrio)):
					if ( HOST != listServswithPrio[x][0]):
						print("Mandando Latido a: " + listServswithPrio[x][0])
						sock.sendto(b"OK", ( listServswithPrio[x][0], ELECPORT ))
						try:#Esperamos respuesta
							data , addr = sock.recvfrom(100)
							cmdArgs = data.decode('utf-8').split()
						except Exception as e:#En caso de error (principalmente timeot)
							print("Exception en EleSocket Coordinador")#Notificamos el error
							print(e)#Continuamos mandando latidos y esperando respuesta
							continue
						if(cmdArgs[0] == "ELECT"):#Estamos atentos a si comienza un proceso de eleccion
							self.Election = True
							self.MasterStatus = False
							print("Mensaje de eleccion recibido")
							self.Bully(sock)
						
			else:
				try:
					data , addr = sock.recvfrom(100)
					cmdArgs = data.decode('utf-8').split()
					print(cmdArgs)
					if(cmdArgs[0] == "OK"): #Latido del coordinador
						#msg = str(clk1.clk.getTimeToNumber())
						#sock.sendto(msg.encode('utf-8'),(addr))
						self.ElectionStatus= False
						sock.sendto(b"OK",(addr))#Regresamos un ok para indicar que funcionamos
					elif(cmdArgs[0] == "ELECT"):#Recibimos notificacion de un proceso de eleccion
						self.Election = True
						self.MasterStatus = False
						print("Mensaje de eleccion recibido")
						self.Bully(sock)
					elif(cmdArgs[0] == "VIC"):#Mensaje de vencedor de eleccion
						#print(addr)#imprimir ip del vencedor
						self.Election = False
						sock.sendto(b"OKVi",(addr))
					elif(cmdArgs[0] == "MYPR"):#En caso de recibir un mensaje de prioridad, este deberia ser de un serv con menor prio por lo que hay que responder
						print("Recibido mensaje de prioridad mayor")
						sock.sendto(b"NO "+ self.prioridad ,(addr))
					elif( cmdArgs[0] == "NO" ):
						print("Respuesta de servidor con mayor prio")
						self.MasterStatus=False
						if (self.prioCount <= 0):
							self.prioCount = 0
						else:
							self.prioCount = self.prioCount - int(cmdArgs[1]) 
					elif( cmdArgs[0] == "OKVi" ):
						self.Election = False
						self.MasterStatus = True
						print("victoria reconocida")
						sock.sendto(b"OK",(addr))
				except socket.timeout as e: #En caso de timeout
					self.prioCount = self.prioCount + 1
					print("Exception en EleSocket")
					print(e)
					print("Prioridad: ")
					print(self.prioCount)
					if ( self.prioridad >= listServswithPrio[0][1]):
						for x in range(0,len(listServswithPrio)):
							if ( HOST != listServswithPrio[x][0]):
								sock.sendto(b"VIC",(listServswithPrio[x][0], ELECPORT))
					elif( self.prioCount > self.prioridad):
						for x in range(0,len(listServswithPrio)):
							if ( HOST != listServswithPrio[x][0]):
								sock.sendto(b"ELECT",(listServswithPrio[x][0], ELECPORT))
					else:
						print("No se recibio respuesta de algun server con mayor prio, ganamos elecciones ")
						for x in range(0,len(listServswithPrio)):
							if ( HOST != listServswithPrio[x][0]):
								print("Mandando Victoria a: " + listServswithPrio[x][0])
								sock.sendto(b"VIC", ( listServswithPrio[x][0], ELECPORT ))
					#elif():			
					#	self.Bully(sock)
					continue



	def Bully(self, EleSocket):
		global listOfServers
		global listServswithPrio
		self.ElectionStatus = True
		self.MasterStatus = False
		print("Entrando a proceso de Elecciones")
		#listServswithPrio=sorted(listServswithPrio, key= lambda x: x[1], reverse= True)#Ordenar lista por prioridad
		#print(listServswithPrio)
		#Checar el primer elemento de la lista, deberia ser el de mayor prioridad
		if(self.prioridad >= listServswithPrio[0][1] ) :#Checamos si tenemos la prioridad mas alta
			#De ser asi, ganamos y mandamos un mensaje de victoria a todos los demas
			BanderaVictoria=True
			print("Soy el de mayor prioridad")
			for k in range(0,len(listServswithPrio)):
				if ( HOST != listServswithPrio[k][0] ):#Mandamos mensaje de victoria a todos menos a nostros mismos
					msg="VIC "+HOST
					print("Mandando Mensaje de Victoria a: " + listServswithPrio[k][0])
					EleSocket.sendto(msg.encode('utf-8'), (listServswithPrio[k][0], ELECPORT) )
					return "victoria por mayor prioridad, servidores notificados"
		else:#En caso de no tener la prioridad mas alta
			for k in range(0,len(listServswithPrio)):#Loopeamos la lista por prioridad
				if (self.prioridad<listServswithPrio[k][1]):#Mandaremos un mensaje a aquellos que tengan prioridad mas alta para saber si podemos ser coordinadores
					print("Mandando prioridad a servers con mayor prioridad: " + listServswithPrio[k][0])
					msg = "MYPR " + str(self.prioridad) #Mensaje de prioridad que mandaremos a aquellos con mator prio
					EleSocket.sendto(msg.encode('utf-8'),(listServswithPrio[k][0], ELECPORT))
					self.prioCount=+1 #Por cada mensaje de prioridad aumentamos el counter
					"""try:
						
					except Exception as e:
						print(e)
						continue"""


	

	def turnOnBackUp(self , IPBackUp):

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


	def listenBackUp(self , clk1):
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

	def listenServer(self , clk1):#Socket y thread para la consistencia de las bases de datos
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			s.bind((HOST , BCKPORT))
			while self.backupEnable:
				data , x = s.recvfrom(1024)
				args = data.decode('utf-8').split()
				self.executeSQLInsert(args[0] , args[1] , args[2] , clk1)



	def RunSocket(self,GUIclk):#Socket manejador de jugadores
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
					print(l)	#Recibiremos una cadena de bytes
					#print (type(l))
					listofData=l.split(b'\n') #Separamos la cadena de bytes por breaklines
					print(listofData)#l ahora es una lista con cadenas de bytes
					for i in range(0, len(listofData)):
						if ( listofData[i].decode("utf-8")=='' ):
							listofData[i]=0
						else:
							listofData[i] = int(listofData[i].decode("utf-8") ) #se decodifica y castea a entero
						totalData = listofData[i]+totalData#Sacar suma de los datos recibidos
						print(totalData)
					print(listofData)
					l = conn.recv(1024)
				print("Termine de recibir")#Notificar que se termino de recibir data
				conn.send(b'Envio Completado')#Mandar mensaje al jugador
				conn.close()
				GUIclk.total = totalData
				hour = str(GUIclk.clk.h).zfill(2) + ":" +str(GUIclk.clk.m).zfill(2)+ ":" +str(GUIclk.clk.s).zfill(2)
				ip = addr[0]

				self.executeSQLInsert(str(totalData) , ip , hour , GUIclk)#Guardar datos
				if(self.backupEnable):  #Mandar al otro server para consistencia
					MGS = str(totalData) + " " + str(ip) + " " + str(hour)
					with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
						print(BKHOST)
						sock.sendto(MGS.encode('utf-8') , (BKHOST , BCKPORT))



	def executeSQLInsert(self , totalData , ip , hour , GUIclk):
		outcome =  (totalData, ip, hour)
		mycursor.execute(sqlformula,outcome)
		mydb.commit()
		GUIclk.lbltotal.config(text = "La suma de los elementos recibidos %d" %int(totalData))

	def listenTime(self , clk1):#Socket e hilo para la sincronizacion de reloj
		sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
		sock.bind((HOST , TIMEPORT))
		sock.settimeout(2)
		print("Time thread empezando")
		while True:
			print(self.ElectionStatus,self.MasterStatus)
			if ( self.ElectionStatus == False and self.MasterStatus == False ):
				try:
					data , addr = sock.recvfrom(100)
					cmdArgs = data.decode('utf-8').split()
					if(cmdArgs[0] == "GTM"): #si llega este mensaje
						msg = str(clk1.clk.getTimeToNumber())#Mandar hora
						sock.sendto(msg.encode('utf-8'),(addr))
					elif(cmdArgs[0] == "CTM"):#Si llega este mensaje
						clk1.clk.setTimeFromNumber(int(cmdArgs[1]))#Ajustar reloj
				except socket.timeout as e:
					print("Timeout in listentime")
				
			elif( self.MasterStatus == True and self.ElectionStatus == False):
				try:
					print("Consulta")
					self.makeAjust(sock, clk1)
					sleep(1)
				except Exception as e:
					print(e)
					print("EXception in timeSOck")
					continue	
			else:
				self.ElectionStatus = False
				sleep(1)





win = tk.Tk()
win.geometry("800x600") #Tamaño de la aplicación
#win.resizable(1,1)	#Esto permite a la app adaptarse al tamaño
clk1 = GUIClock(win,0,0)	#iniciamos el reloj maestro en la posicion 0, 0
com = Comunicator(clk1,BKHOST)
win.mainloop()
