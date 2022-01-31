import threading
import sys
import socket
import pickle
import os
import ipaddress
import json

class Cliente():

	def __init__(self, host=socket.gethostname(), port=59989):
		self.sock = socket.socket()
		host_aux = input('\nEscriba la direccion Ip o pulse enter para utilizar la direccion local\n')
		try:
			host = ipaddress.ip_address(host_aux)
		except:
			host=socket.gethostname()
		port_aux = input('\nEscriba el puerto o pulse enter para utilizar el puerto por defecto\n')
		if port_aux.isdigit() and int(port_aux) > 0 and int(port_aux) < 65000:
			port = int(port_aux)
		nickname = input('\nEscriba un nickname\n')
		self.sock.connect((str(host), int(port)))
		hilo_recv_mensaje = threading.Thread(target=self.recibir)
		hilo_recv_mensaje.daemon = True
		hilo_recv_mensaje.start()
		print('Hilo con PID',os.getpid())
		print('Hilos activos', threading.active_count())
		self.enviar("nickname:"+str(nickname))

		while True:
			texto = input('\nEscriba texto ? ** Enviar = ENTER ** Abandonar Chat = Q \n')
			if texto != 'Q' :
				self.enviar(nickname +":"+texto)
			else:
				print(" **** TALOGOOO  ****")
				self.sock.close()
				sys.exit()
	def recibir(self):
		while True:
			try:
				data = self.sock.recv(32)
				if data:
					print(pickle.loads(data))
			except:
				pass

	def enviar(self, msg):
		self.sock.send(pickle.dumps(msg))

c = Cliente()

		