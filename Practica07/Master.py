import socket
import mysql.connector
from time import sleep
import threading

class Master:
	def __init__(self):
		self.listOfServers = ["-1"]*256
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		self.IP = s.getsockname()[0]
		self.PORT = 60428
		s.close()
		self.isCordinator = False
		self.cordinador = Cordinador(self.listOfServers,self.IP)
		self.sincronizador = Sincronizador()


	def Run(self):
		print("Master isRunning")
		Flag = True
		print("Running mapOfServers")
		isOneEnable = self.cordinador.mapListOfServers()
		sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
		sock.bind((self.IP , self.PORT))
		sock.settimeout(5.0)
		print("Calling for cordinator")		
		if(isOneEnable == "-1"):
			self.cordinador.cordinadorIP = self.IP
		else:
			while Flag:
				for i in range(254):
					if(self.listOfServers[i] == "-1"):
						continue
					print("Who is cordinator. %d  -> %s" % (i , self.listOfServers[i]))
					try:
						sock.sendto(b'GMC' ,(self.listOfServers[i],self.cordinador.PORT))
						data , addr = sock.recvfrom(100)
						self.cordinador.cordinadorIP = data.decode('utf-8')
					#	print("LLego esto %s " % self.cordinador.cordinadorIP)
						if(self.cordinador.cordinadorIP != "-1"):
							Flag = False
					except socket.timeout as ex:
				#		print("NRL")
						pass

		cordListenThread = threading.Thread(target=self.cordinador.cordinadorListener)
		cordListenThread.setDaemon(True)
		cordListenThread.start()		

		while not self.isCordinator:
			if(self.cordinador.cordinadorIP == self.IP):
				self.isCordinator = True
				break
			print("I am not the cordinator")
			try:
				print(self.cordinador.cordinadorIP)
				sock.sendto(b"AYE" ,(self.cordinador.cordinadorIP,self.cordinador.PORT))
				data , addr = sock.recvfrom(100)
				msg = data.decode('utf-8').split()
				if(msg[0] == "YBR"):
					sleep(10.0)
			except socket.timeout as ex:
				self.cordinador.Eleccion()
	

		print("I am cordinator")
		self.sincronizador.start(self.listOfServers,self.IP)


		

class Cordinador:
	def __init__(self, listOfServers,IP):
		self.listOfServers = listOfServers
		self.IP = IP
		self.PORT = 60430
		self.cordinadorIP = "-1"
		
#	def findEnableServers():
#		print("Declare subNet")
#		IPx = input()
#		for i in range(2,250):

	def Eleccion(self):
		dominios = self.IP.split('.')
		AuxIp = dominios[0] + '.' + dominios[1] + '.' + dominios[2] + '.'
		sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
		sock.settimeout(0.05)
		isOneEnable = False
		for i in range(int(dominios[3]),254):
			if(AuxIp + str(i) == self.IP):
				continue
			try:
				sock.sendto(b'AYE',(AuxIp + str(i) , self.PORT))
				data , addr = sock.recvfrom(100)
				msg = data.decode('utf-8').split()
				if(msg[0] == "YBR"):
					isOneEnable = True
					break;
			except socket.timeout as ex:
				pass
		self.mapListOfServers()
		if(not isOneEnable):
			self.cordinadorIP = self.IP
			for i in range(2,254):
				if(self.listOfServers[i] != "-1"):
					sock.sendto(b'SEC',(self.listOfServers[i] , self.PORT))
		sock.close()
		while(self.cordinadorIP == "-1"):
			sleep(1.0)			


	def mapListOfServers(self):
		dominios = self.IP.split('.')
		AuxIp = dominios[0] + '.' + dominios[1] + '.' + dominios[2] + '.'
		sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
		sock.settimeout(0.1)
		isOneEnable = "-1"
		for i in range(2,254):
		#	sleep(0.01)
			if(AuxIp + str(i) == self.IP):
				continue
			try:
			#	print(AuxIp + str(i))
				sock.sendto(b'AYE',(AuxIp + str(i) , self.PORT))
				data , addr = sock.recvfrom(100)
				msg = data.decode('utf-8').split()
				if(msg[0] == "YBR"):
					isOneEnable = "1"
			#		print("Si toy %s" % (AuxIp + str(i)))
					self.listOfServers[i] = AuxIp + str(i)
			except socket.timeout as ex:
				self.listOfServers[i] = "-1"
		sock.close()
		return isOneEnable

	def cordinadorListener(self):
		sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
		sock.bind((self.IP , self.PORT))
		while True:
			data , addr = sock.recvfrom(100)
			cmdArgs = data.decode('utf-8').split()
			print(cmdArgs[0])
			if(cmdArgs[0] == "AYE"):
				self.listOfServers[self.getIpIndex(addr[0])] = addr[0]
				sock.sendto(b'YBR',(addr))
			elif(cmdArgs[0] == "MLLE"):
				self.cordinadorIP = "-1"
				sock.sendto(b'YBR',(addr))
			elif(cmdArgs[0] == "SEC"):
				self.cordinadorIP = addr[0]
			elif(cmdArgs[0] == "GMC"):
				sock.sendto(self.cordinadorIP.encode('utf-8'),(addr))
			elif(cmdArgs[0] == "SNA"):
				replicThread = threading.Thread(target=self.replicacion)
				replicThread.start()

	def replicacion(self):
		totalData=0
		listofData = b''
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #Creamos el socket le ponemos el nombre de s, AF_INET=IPV4 SOCK_STREAM=TCP
			while True:
				try:
					s.bind((self.IP, self.PORT-3))#Publicamos la ip y puerto
					s.listen(4)#Aceptaremos maximo 4 conexiones
					conn, addr = s.accept() #Aceptar la conexion
					break
				except socket.timeout as ex:
					pass	
			print(f"Conection desde {addr} ha sido establecida")
			conn.send(bytes("Conectado a servidor", "utf-8"))
			totalData=0
			l = conn.recv(4294967296)
			while (l): #Mientras l reciva algo entrara en este loop
				print("Recibiendo...")
			#	print(l)	#Recibiremos una cadena de bytes
				#print (type(l))
				listofData += l
			#	print(listofData)
				l = conn.recv(4294967296)
			print("Termine de recibir")
			conn.send(b'Envio Completado')
			conn.close()
			s.close
			s.shutdown(socket.SHUT_WR)

		sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)		
		for i in range (2,250):
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			block = 0
			if(self.listOfServers[i] == "-1" or self.listOfServers[i] == self.IP):
				continue
			try:
				sock.sendto(b'AYE' , (self.listOfServers[i] , self.PORT))
				ans , addr = sock.recvfrom(100)
			except socket.timeout as ex:
				self.listOfServers[i] = "-1"
				continue
			s.connect((self.listOfServers[i], 65432))
			#time.sleep(0.001)
			print("Enviando...")
			l = listofData[block*4294967296:block*4294967296+4294967295]
			while (l):
				block += 1
				print("Enviando...")
				s.send(l)
				l = listofData[block*4294967296:block*4294967296+4294967295]
			print("Envio Completado")
		#	print (s.recv(4294967296))
			s.close
			s.shutdown(socket.SHUT_WR)

	def getIpIndex(self , IP):
		dominios = IP.split('.')
		return int(dominios[3])


class Sincronizador:
	
	def __init__(self):
		self.PORT = 60432
	#	self.mydb = mysql.connector.connect(
	#		host="localhost",
	#		user="root",
	#		password="root",
	#		database="Tiempo"
	#	)
	#	self.mycursor = self.mydb.cursor()

	def toTime(self,num):
		cadena = ""
		cadena += str(num//10000)+":"
		num -= (num//10000)*10000
		cadena += str(num//100)+":"
		num -= (num//100)*100
		cadena += str(num)
		return cadena

	def makeAjust(self,sock , listOfServers , IP):
		prom = 0
		enables = 1
		sock.sendto(b'GTM',(IP,self.PORT))
		data , addr = sock.recvfrom(100)
		prom += int(data.decode('utf-8'))
		if(len(listOfServers) > 0):
			for x in listOfServers:
				if(x != "-1"):
					print("[%s , %d]" % (x , self.PORT) )
					enables += 1
					sock.sendto(b'GTM',(x,self.PORT))
					data , addr = sock.recvfrom(100)
					prom += int(data.decode('utf-8'))
					print(prom)
			prom = prom // enables
			MSG = "CTM " + str(prom)
			hora = self.toTime(prom)
		#	sqlformula = "INSERT INTO Tiempo (hora) VALUES(\"%s\")"
		#	self.mycursor.execute(sqlformula,(hora,))
	#		self.mydb.commit()
			sock.sendto(MSG.encode('utf-8'),(IP,self.PORT))
			for x in listOfServers:
				if(x != "-1"):
					sock.sendto(MSG.encode('utf-8'),(x,self.PORT))
			

	def start(self,listOfServers,IP):


		sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
		sock.bind((IP,self.PORT-1))
	#	sock.settimeout(0.5)

		while True:
			try:
				print("Consulta")
				self.makeAjust(sock,listOfServers,IP)
				sleep(10.0)
			except KeyboardInterrupt as k:
				break
