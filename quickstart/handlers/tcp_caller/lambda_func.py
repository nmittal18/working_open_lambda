import requests
import sys
import json
import socket
import os
import time
from subprocess import call


def child():
	time.sleep(5)
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Connect the socket to the port where the server is listening
	server_address = ('172.17.0.2', 8089)
	sock.connect(server_address)
	
	fg = open("server_response", 'wb') 
	
	try:
	    # Send data
	    message = 'This is the message.  It will be repeated.'
	    sock.sendall(message)
	
	    # Look for the response
	    amount_received = 0
	    amount_expected = len(message)
	
	    while amount_received < amount_expected:
	        data = sock.recv(16)
	        amount_received += len(data)
		fg.write(data)
	finally:
	    sock.close()
	    fg.close()

	#exiting the child process
	os._exit(0)


def handler(conn, event):
    try:
	newpid = os.fork()
        if newpid == 0:
           child()
        else:

          f = open("x", 'wb')
          g = open("y", 'wb')

	  #call perf
          call(["perf","record", "-e", "syscalls:sys_*", "-e", "net:*", "-e", "skb:*" ,"-e", "sock:*" ,"-e", "cpu-clock","-F", "99","--output=perf_socket_ver1.data", "-a", "-g", "-p", str(newpid) ], stdout=f, stderr=g)

    	  #wait for child      
	  done = os.waitpid(newpid,0)
          f.write("child pid" + str(newpid))
          f.write(str(done))

	  #perf script	
          perf_output = open("socket_perf_output", 'wb')
          call(["perf", "script", "--input=perf_socket_ver1.data"], stdout=perf_output, stderr=g)

	  #close all files
          perf_output.close()
          f.close()
          g.close()
	
	  #open stdout and stderr for reading
          f = open("x", 'rb')
          g = open("y", 'rb')
          return str(f.read()) + str(g.read()) + "How are you, %s!" % event['name']
    except Exception as e:
        return {'error': str(e)}
