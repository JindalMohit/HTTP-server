# this is client 
import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

# get local machine name
host = socket.gethostname();
port = 9999

# connection to hostname on the port
s.connect((host, port))

# recieve a msg of n bytes
n = 1024
msg = s.recv(n)

# end the connection
s.close()

print(msg.decode('ascii'))