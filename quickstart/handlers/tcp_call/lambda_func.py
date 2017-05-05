import socket 
from time import sleep
import os
import json
import sys
import string
import time
import random
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

def handler(conn, event):
#def handler():
    try:
	port = int(event['port'])
	#port = 4578
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect(("localhost", port))
	except socket.error, e:
		if 'Connection refused' in e:
			return {'error':'*** Connection refused ***'}

	k = event.get('num_keys',1)
        d = event.get('depth', 1)
        l = event.get('value_len', 1)
        i = event.get('iterations', 100)

        fd = open("tcp_run_" + str(l) + ".txt", 'wb')
        data = random_dict(num_keys=k, depth=d, value_len=l)
        tmp = pickle.dumps(data)
        payload = json.dumps(data)
        minTime = sys.maxsize
        totalTime = 0

        for _ in range(i):
                start = time.time()
                sock.sendall(payload)
                ret = sock.recv(16)
                end = time.time()
		fd.write("ret" + str(ret))
                elapsed = end - start
                totalTime = totalTime + elapsed
                if minTime > elapsed:
                        minTime = elapsed
                fd.write("Time elapsed =" + str(elapsed)+ "\n")
        avgTime = totalTime/i
        sock.close()
        fd.write("Average Time =" + str(avgTime)+ "\n")
        fd.write("minTime =" + str(minTime)+ "\n")
        fd.close()
        return "What's up, %s!" % event['name']
    except Exception as e:
        return {'error': str(e)}
 
#def main():
#       handler()
#
#if __name__== "__main__":
#  main()

# def handler(conn, event):
#     try:
#       port = int(event['port'])
# 
#       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#       #sock.bind("172.17.0.1", port)
#       sock.connect(("0.0.0.0", port))
#       return "Call: done"
#     except Exception as e:
#         return {'error': str(e)} 
