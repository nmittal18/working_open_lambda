import socket
import sys
import os

def handler(conn, event):
#def handler():
    try:
	# Make sure the socket does not already exist
	server_address = '/home/ubuntu/uds1.sock'
	try:
		os.unlink(server_address)
	except OSError:
		if os.path.exists(server_address):
        		raise
	f = open("hello_output_3", 'w')
	f.write('write' )
	# Create a UDS socket
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	# Bind the socket to the port
	f.write('starting up on %s' % server_address)
	sock.bind(server_address)
	
	# Listen for incoming connections
	sock.listen(1)

	while True:
	    # Wait for a connection
	    f.write('waiting for a connection')
	    connection, client_address = sock.accept()
	    try:
	        f.write('connection from ',  client_address)
	
	        # Receive the data in small chunks and retransmit it
	        while True:
	            data = connection.recv(16)
	            f.write('received "%s"' % data)
	            if data:
	                f.write('sending data back to the client')
	                connection.sendall(data)
	            else:
	                f.write('no more data from ',  client_address)
	                break
	            
	    finally:
	        # Clean up the connection
	        connection.close()
		f.close()
        return "Hello, %s!" %data
    except Exception as e:
        return {'error': str(e)}

#def main():
#       handler()
#
#if __name__== "__main__":
#  main() 
