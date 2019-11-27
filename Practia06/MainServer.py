import threading
from Server import Server
from Master import Master

master = Master()
masterProcess = threading.Thread(target=master.Run)
masterProcess.setDaemon(True)
masterProcess.start()
serv = Server()