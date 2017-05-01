# IPC call
# Paired with IPC_resp
# This bench does the following:
#       1) Open mq (already setup by resp)
#       2) Send msg
#       3) Wait for resp
#       4) Exit

# This timing is unfair wrt the curl bench: 
# Resp sets up the channel and call just opens it, so this bench doesn't include setup time
# This is tricky to coordinate, since benches must be setup using http messages

from subprocess import call
from time import sleep
import os
import json
import sys
from posix_ipc import *
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
    try:
        k = event.get('num_keys',1)
        d = event.get('depth', 1)
        l = event.get('value_len', 1)
        i = event.get('iterations', 100)

	fd = open("ipc_latency_run_" + str(l) + ".txt", 'wb')
        data = random_dict(num_keys=k, depth=d, value_len=l)
	tmp = pickle.dumps(data)
	payload = json.dumps(d)
        minTime = sys.maxsize
        totalTime = 0

	for _ in range(i):
		start = time.time()
		mq = MessageQueue("/mytest", flags=O_CREAT, mode=0600, max_messages = 8, max_message_size=len(tmp.encode('utf-8')))
		#mq = MessageQueue("/mytest")
		mq.send(payload)
		ret = mq.receive()
	        mq.close()
	        mq.unlink()
		end = time.time()
		call(["rm", "-f", "/dev/mqueue/mytest"])
                elapsed = end - start
                totalTime = totalTime + elapsed
                if minTime > elapsed:
                        minTime = elapsed
                fd.write("Time elapsed =" + str(elapsed)+ "\n")
        avgTime = totalTime/i
        fd.write("minTime =" + str(minTime)+ "\n") 
        fd.write("Average Time =" + str(avgTime)+ "\n")
        fd.close()
        return "What's up, %s!" % event['name']
    except Exception as e:
        return {'error': str(e)} 
