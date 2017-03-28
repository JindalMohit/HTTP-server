#! /usr/bin/python
# HTTP server using object-oriented approach
# without gui : it is creating confusion and errors
# also implement response_headers properly
# also implement POST request by to-night
import socket
import signal
import sys
import threading
from threading import Thread

class Server(object):
	"""doc string for the server"""
	def __init__(self):
		self.host = '172.25.14.62'
		self.port = 8888

	def activate_server(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# assign a port to the socket
		try:
			self.socket.bind((self.host, self.port))
			print("Launching HTTP server at ", self.host, ":", self.port)
		except Exception as e:
			print (e)
			sys.exit()
		print("Server successfully acquired the socket with port:", self.port)
		print("Press ctrl+c to close the server.\n")
		# handle this keyboard_interrupt
		self.listen_client()

	def listen_client(self):
		# start TCP listen
		# set number of request in the queue
		# later if time permits do scheduling and multi-threading
		n = 5
		self.socket.listen(n)
		while True:
			# now a request from a client for a connection has arrived
			# accept the TCP connection
			c_socket, c_addr = self.socket.accept()
			print("Got a connection from ", c_addr)
			# extrac the information data from the client socket
			data = c_socket.recv(1024)
			# 1024 byte size data is received
			self.handle_request(c_socket, data)
			print("")
			c_socket.close()

	def handle_request(self, client_socket, client_data):
		msg = ""
		print("Following data received from client:")
		print(client_data.decode('ascii'))
		data = client_data.split( )
		request_method = ""
		request_path = "/"
		http_version = ""
		try:
			request_method = data[0]
			request_path = data[1]
			http_version = data[2]
		except Exception as e:
			print (e)
		# handle GET request
		if(request_method == 'GET'):
			if(request_path == '/'):
				request_path = '/index.html'
			path = 'Resources' + request_path
			file_type = request_path.split('.')[1]
			if(file_type == 'php'):
				path = '/var/www/html' + request_path
			if(request_path == '/favicon.ico'):
				print("favicon.ico request")
				client_socket.send('HTTP/1.1 200 OK\r\n')
				client_socket.send('Content-Length: 318\r\n')
				client_socket.send('Connection: close\r\n')
				client_socket.send('Content-Type: image/x-icon\r\n\r\n')
				File = open(path, 'rb')
				msg = File.read()
				client_socket.send(msg)
			else:
				print('Request path: ',request_path)
				msg = ""
				try:
					File = open(path, 'rb')
					msg += 'HTTP/1.1 200 OK\r\n'
				except Exception as e:
					path = 'Resources/error.html'
					File = open(path, 'rb')
					msg += 'HTTP/1.1 404 ERROR\r\n'
					msg += File.read()
					File.close()
				if(file_type == 'jpg'):
					msg += 'Content-Type: image/x-icon\r\n\r\n'
				msg += File.read()
				File.close()
				client_socket.send(msg)
		# handle POST request
		if(request_method == 'POST'):
			#print(client_data.decode('ascii'))
			data = ""
			try:
				data = client_data.split('\r\n\r\n')[1]
			except Exception as e:
				print e
				data = ""
			print("Data received: \n", data)
			msg = "HTTP/1.1 200 OK\r\n\nThanks for connecting."
			client_socket.send(msg)

s = Server()
s.activate_server()