import socket

# create a new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

# get the local machine name
host = '172.25.14.62';
# host is basically my pc name: mohit-HP-15-Notebook-PC

# set a port for connection
port = 8000

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
	msg='Thank you for connecting\n';
	client_socket.send(msg.encode('ascii'))
	client_socket.close()