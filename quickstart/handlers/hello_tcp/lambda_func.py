import socket
import sys
import os

def handler(conn, event):
#def handler():
    try:
	f = open("hello_output", 'wb')
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Bind the socket to the port
	f.write("socket address == ")
	#server_address = ('http://172.17.0.1', 8089)
	server_address = ('0.0.0.0', 4567)
	f.write(str(server_address))
	f.write("==== ")
	sock.bind(server_address)
	f.write("binding done")
	# Listen for incoming connections
	sock.listen(1)
	f.write("listening")

	while True:
	    f.write("waiting")
	    # Wait for a connection
	    connection, client_address = sock.accept()
    	    try:
           	 # Receive the data in small chunks and retransmit it
           	 while True:
           	     data = connection.recv(16)
           	     if data:
			 f.write(data)
           	         connection.sendall(data)
           	     else:
           	         break
            finally:
        	 # Clean up the connection
        	 connection.close()
	f.write("exiting")
	#os.exit(0)
        return "Hello, %s!" %data
    except Exception as e:
        return {'error': str(e)}

#def main():
#       handler()
#
#if __name__== "__main__":
#  main() 
