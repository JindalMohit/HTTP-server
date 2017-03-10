import socket

class Client():
	def __init__(self, port = 8000):
		self.port = port
		self.host = '172.25.14.62'

	def set_connection(self):
		#create a socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.socket.connect((self.host, self.port))

	def receive_msg(self):
		"""msg = self.socket.recv(1024)
		print(msg.decode('ascii'))"""
		self.req_method = raw_input("Enter request or 'end' to end connection: ")
		while self.req_method != 'end':
			print(self.req_method)
			self.socket.send(self.req_method)
			self.req_method = raw_input("Enter request or 'end' to end connection: ")
		self.end_connection()	

	def end_connection(self):
		self.socket.close()

c = Client(8888)
c.set_connection()
c.receive_msg()

