# HTTP server using object-oriented approach
import socket
import sys
from gi.repository import Gtk as gtk
import threading
from threading import Thread

class Server(object):
	"""docstring for Server"""
	def __init__(self, port = 8000):
		self.host = '127.0.0.1'
		self.port = port
		self.output = ""
		self.th = False

	def activate_server(self):
		while not self.th:
			pass
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# assign a port to the socket
		try:
			self.socket.bind((self.host, self.port))
			print("Launching HTTP server at ", self.host, ":", self.port)
			self.output += "Launching HTTP server at " +str(self.host) + ":" + str(self.port)
		except Exception as e:
			print (e)
			self.output += str(e)
			sys.exit()
		print("Server successfully acquired the socket with port:", self.port)
		self.output += "Server successfully acquired the socket with port:" + str(self.port)
		print("Press ctrl+c to close the server.")
		self.output += "Press ctrl+c to close the server."
		self.listen_client()

	def deactivate_server(self):
		if(self.th):
			self.th = False

	def is_activated(self):
		return self.th

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
			self.output += "Got a connection from " + str(c_addr)
			#msg = "Thank you for connecting\n"
			#c_socket.send(msg.encode('ascii'))

			# extract the data from the client socket
			print ("hello")
			data = c_socket.recv(1024)
			print(data.decode('ascii'))
			self.output += data.decode('ascii')

			self.handle_request(c_socket, data)

			c_socket.close()

			if  not self.th:
				break
		while not self.th:
			pass
		self.listen_client()

	def get_response_header(self, http_version, status_code):
		h = http_version + " "
		if(status_code == 200):
			h += "200 OK\n"
		elif(status_code == 404):
			h += "404 Not Found\n"
		return h.encode()

	def handle_request(self, client_socket, client_data):
			data = client_data.split( )
			request_method = data[0]
			
			try:
				request_path = data[1]
			except Exception as e:
				print (e)
			try:
				http_version = data[2]
			except Exception as e:
				print (e)

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


class Gui():
	def __init__(self):
		self.frame = gtk.Window()
		self.frame.set_default_size(600, 300)
		self.frame.connect("delete-event", gtk.main_quit)
		self.frame.set_title("HTTP-Server")
		self.add_buttons()
		self.place_widgets()

	def add_buttons(self):
		self.start_b = gtk.Button("Start")
		self.start_b.set_size_request(70, 30)
		self.start_b.connect("clicked", self.start_handler)
		self.restart_b = gtk.Button("Restart")
		self.restart_b.connect("clicked", self.restart_handler)
		self.stop_b = gtk.Button("Stop")
		self.stop_b.connect("clicked", self.stop_handler)
		self.end_b = gtk.Button("End")
		self.end_b.connect("clicked", self.end_handler)

	def place_widgets(self, str="Welcome"):
		self.vb = gtk.VBox(False, 1)
		self.vb.add(self.start_b)
		self.vb.add(self.restart_b)
		self.vb.add(self.stop_b)
		self.vb.add(self.end_b)

		self.hb = gtk.HBox(False, 6)
		self.hb.add(self.vb)
		self.board = gtk.TextView()
		self.hb.add(self.board)

		self.text = gtk.TextBuffer()
		# now the only task remaining is to add the content in text
		#str = "Yipee! Finally working."
		
		#modify next 2 lines
		#self.text.set_text(str.encode('utf-8'))
		#self.board.set_buffer(self.text)

		self.frame.add(self.hb)
		self.frame.show_all()

	def start_handler(self, widget):
		if(s.is_activated()):
			print("Server is already started")
		else:
			print("Starting HTTP server")
			try:
				s.th = True
			except Exception as e:
				print (e)
	def restart_handler(self, widget):
		pass
	def stop_handler(self, widget):
		if(s.is_activated()):
			s.deactivate_server()
	def end_handler(self, widget):
		sys.exit()


s = Server(8888)
o1 = Gui()
thread_gui = Thread(name='thread_gui', target=gtk.main, args=())
thread_server = Thread(name='thread_server', target=s.activate_server, args=())
thread_gui.start()
thread_server.start()