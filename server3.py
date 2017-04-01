#! /usr/bin/python
# HTTP server using object-oriented approach
# without gui : it is creating confusion and errors
# also implement response_headers properly
# also implement POST request by to-night
import socket
import signal
import sys
import subprocess
import threading
from threading import Thread
import cgi, cgitb
import cStringIO
from cStringIO import StringIO
import mysql.connector
from mysql.connector import errorcode
import getpass
import os

class Server(object):
	"""doc string for the server"""
	def __init__(self):
		# self.host = '172.25.14.62'
		self.host = '127.0.0.1'
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
					msg += File.read()
					File.close()
				except Exception as e:
					print e
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
			path = '/usr/lib' + request_path
			try:
				"""print 'PAY ATTENTION TO HEADERS:'
				print client_data.split('\r\n\r\n')[0]
				print 'END'"""
				data2 = StringIO(data)
				form = cgi.FieldStorage(fp=data2, headers=client_data.split('\r\n\r\n')[0], environ={'REQUEST_METHOD':'POST'}) 
				# Get data from fields
				first_name = form.getvalue('first_name')
				last_name  = form.getvalue('last_name')
				gender  = form.getvalue('gender')
				# print 'work a'
				add_user = ("INSERT INTO user "
				"(first_name, last_name, gender) "
				"VALUES (%s, %s, %s)")
				# print 'work b'
				data_user = (first_name, last_name, gender)
                # Insert new user
				cursor.execute(add_user, data_user)
				# Make sure data is committed to the database
				cnx.commit()
				# print 'work c'
				"""msg = "HTTP/1.1 200 OK\r\n\nThanks for connecting."
				client_socket.send(msg) """
				msg = "HTTP/1.1 200 OK\r\n\n"
				#msg += "Content-type:text/html\r\n\r\n"
				msg += "<!DOCTYPE html>"
				msg += "<html>"
				msg += "<head>"
				msg += "<title>Hello - Second CGI Program</title>"
				msg += "</head>"
				msg += "<body>"
				msg += "<h2>%s %s, your response has been recorded.</h2>" % (first_name, last_name)
				msg += "</body>"
				msg += "</html>"
				# print 'work d'
				client_socket.send(msg)
				# print 'working1'
			except Exception as e:
				print e
				path = 'Resources/error.html'
				File = open(path, 'rb')
				msg += 'HTTP/1.1 404 ERROR\r\n'
				msg += File.read()
				File.close()
				# print 'working2'
				client_socket.send(msg)
		#handle DELETE request
		if(request_method == 'DELETE'):
			if(request_path == '/'):
				client_socket.send('HTTP/1.1 200 OK\r\n')
				client_socket.send('You have not given any file name to delete.\nRequest discarded.')
			else:
				path = 'Temp' + request_path
				print('Request path: ',request_path)
				msg = ""
				try:
					os.remove(path)
					msg = ""
					msg += 'HTTP/1.1 404 ERROR\r\n'
					path = 'Resources/del_success_msg.html'
					File = open(path, 'rb')
					msg += File.read()
					File.close()
					client_socket.send(msg)
				except Exception as e:
					if e.errno == 21:
						try:
							shutil.rmtree(path)
						except Exception as e:
							if e.errno == 2:
								self.error_404(client_socket)
							else:
								print e
								self.error_500(client_socket)
					elif e.errno == 2:
						self.error_404(client_socket)
					else:
						print e
						self.error_500(client_socket)


	def error_404(self, client_socket):
		msg = ""
		path = 'Resources/error.html'
		File = open(path, 'rb')
		msg += 'HTTP/1.1 404 ERROR\r\n'
		msg += File.read()
		File.close()
		client_socket.send(msg)

	def error_500(self, client_socket):
		msg = ""
		path = 'Resources/error500.html'
		File = open(path, 'rb')
		msg += 'HTTP/1.1 500 Internal Server Error\r\n'
		msg += File.read()
		File.close()
		client_socket.send(msg)
			


s = Server()
s.activate_server()

print('Connecting to database:')
try:
  password = getpass.getpass('Enter your mysql password: ')
  cnx = mysql.connector.connect(user='root', password=password, database='My_http_server')
  print("Successfully connected to database\n")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

cursor = cnx.cursor()

# Both server and database is set-up now
# Start listening the client requests
print("Ready to receive requests....")
s.listen_client()
cursor.close()
cnx.close()