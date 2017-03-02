import socket # for networking support
import signal # for signal support
import time   # current time

# create a new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

# get the local machine name
host = '172.25.14.62';
# host is basically my pc name: mohit-HP-15-Notebook-PC

# set a port for connection
port = 8888

# bind socket to the port
s.bind((host, port))

# start TCP listen
# set no. of request in queue
n = 2
s.listen(n);

while True:
	# now a request for a connection has arrived
	# accept the connection
	client_socket, client_addr = s.accept();

	print("Got a connection from %s\n" %str(client_addr))

	# send a welcome message to the client
	msg='Thank you for connecting\n';
	client_socket.send(msg.encode('ascii'))
	
	# receive data from the client_socket
	client_data = client_socket.recv(1024)
	# decode it to string
	string = bytes.decode(client_data)
	# extract the request type
	request_method = string.split(" ")[0]
	#print("Request method: %s\n" %request_method)
	#print("Request body: %s\n" %string)
	if (request_method == 'GET'):
		body = string.split(" ")
		file_requested = body[1]
		print("file_requested: %s" %file_requested)
		file_path = "Resources" + file_requested
		print("file path: %s" %file_path)

		# send the requested resource
		File = open(file_path, 'r')
		client_socket.send(File.read())
	client_socket.close()





