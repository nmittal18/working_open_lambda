import socket 
import random
import json
import os
import sys
import string
import time
import cPickle as pickle
from sys import getsizeof


def random_string(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))



# keys^depth values
def random_dict(num_keys, depth, value_len):
    d = {}
    for _ in range(num_keys):
        if depth < 2:
            d[random_string(8)] = random_string(value_len)
        else:
            d[random_string(8)] = random_dict(num_keys, depth-1, value_len)

    return d

#sock_addr = ("localhost", 4578)

def handler(conn, event):
#def handler():
    try:
	port = int(event['port'])
	l = event.get('value_len', 1)
	#sock_addr = ("localhost", port)
	i = 0
	fd = open("tcp_resp_" + str(l) + ".txt", 'w')
	data = random_dict(num_keys=1, depth=1, value_len=l)
	payload = json.dumps(data)
	size = getsizeof(payload)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#sock.bind(sock_addr) 
	sock.bind(("localhost", port)) 
	fd.write("bind")
	sock.listen(1)
	fd.write("listen")
	connection, client_address = sock.accept()
	while i < 100:
		while True:
			data1 = connection.recv(size)
			if not data1: break
		connection.send("Ack")
		i = i+1
	fd.close()			
	connection.close()
	return "Hello, Neha!" 
    except Exception as e:
        return {'error': str(e)}


#def main():
#       handler()
#
#if __name__== "__main__":
#  main()


#	while True:
#	     # Wait for a connection
#	  connection, client_address = sock.accept()
#          try:
#               # Receive the data in small chunks and retransmit it
#               while True:
#                   data = connection.recv(size)
#                   if data:
#                       f.write(data)
#                       connection.send("Ack")
#                   else:
#                       break
#          finally:
#               # Clean up the connection
#               connection.close()
#	       fd.close()
#        return "Hello, %s!" %data
#    except Exception as e:
#        return {'error': str(e)}


          

