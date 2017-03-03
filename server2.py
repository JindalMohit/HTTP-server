# HTTP server using object-oriented approach
import socket
import sys

class Server(object):
	"""docstring for Server"""
	def __init__(self, port = 80):
		self.host = '172.25.14.62'
		self.port = port

	def activate_server(self):
		#create a socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# assign a port to the socket
		try:
			self.socket.bind((self.host, self.port))
			print("Launching HTTP server at ", self.host, ":", self.port)
		except Exception as e:
			print("User specified port is unavailable, trying to connect with port:80")
			try:
				self.port = 80
				self.socket.bind((self.host, self.port))
				print("Launching HTTP server at ", self.host, ":", self.port)
			except Exception as e:
				print("Port:", self.port, " is unavailable, trying to connect with port:8008")
				try:
					self.port = 8008
					self.socket.bind((self.host, self.port))
					print("Launching HTTP server at ", self.host, ":", self.port)
				except Exception as e:
					print("Port:", self.port, " is unavailable, trying to connect with port:8080")
					try:
						self.port = 8080
						self.socket.bind((self.host, self.port))
						print("Launching HTTP server at ", self.host, ":", self.port)
					except Exception as e:
						print("ERROR: Unable to assign a port to the socket.")
						sys.exit()
		print("Server successfully acquired the socket with port:", self.port)
		print("Press ctrl+c to close the server.")
		self.listen_client()

	def listen_client(self):
		# start TCP listen
		# set no. of requests in queue
		n = 5
		self.socket.listen(n)
		while True:
			# now a request from a client for a connection has arrived
			# accept the connection
			c_socket, c_addr = self.socket.accept()
			print("Got a connection from ", c_addr)
			#msg = "Thank you for connecting\n"
			#c_socket.send(msg.encode('ascii'))

			# extract the data from the client socket
			data = c_socket.recv(1024)
			print(data.decode('ascii'))

			self.handle_request(c_socket, data)

			c_socket.close()

	def get_response_header(self, http_version, status_code):
		h = http_version + " "
		if(status_code == 200):
			h += "200 OK\n"
		elif(status_code == 404):
			h += "404 Not Found\n"
		return h.encode()

	def handle_request(self, client_socket, client_data):
			data = client_data.split(" ")
			request_method = data[0]
			request_path = data[1]
			http_version = data[2]

			if(request_method == 'GET'):
				path = 'Resources' + request_path
				msg = ""
				try:
					File = open(path, 'rb')
					msg += self.get_response_header(http_version, 200)
					msg += File.read()
					File.close()
				except Exception as e:
					msg += self.get_response_header(http_version, 404)
				
				client_socket.send(msg)


print("Starting HTTP server")
# create a Server object
s = Server(8888)
# activate the Server
s.activate_server()