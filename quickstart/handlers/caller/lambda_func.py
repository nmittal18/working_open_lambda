import requests
#import sys
import json
import string
import random
import time
from subprocess import call

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
	payload = json.dumps({'name':'Neha'})
	f = open("x", 'w')
	g = open("y", 'w')
        call(["perf","record", "-e", "syscalls:sys_*", "-e", "net:*", "-e", "skb:*" ,"-e", "sock:*" ,"-e", "cpu-clock","-F", "99","--output=perf.data", "-a", "-g", "--","curl", "http://172.17.0.1:8085/runLambda/hello", "-d", "{ }" ], stdout=f, stderr=g)
	perf_output = open("perf_output", 'wb')
	call(["perf", "script", "--input=perf.data"], stdout=perf_output, stderr=g)
        f.close()
        g.close()
	perf_output.close()
        f = open("x")	
	g = open("y")
    	return "stdout = " + f.read() +"stderr =" + g.read()

        #payload = {'name': 'Neha'}
        #r = requests.post("http://172.17.0.1:8081/runLambda/hello", data=payload)
        #logging.debug(r.status_code)
        #logging.debug(r.content)
        #return str(json.loads(f.read)) + str(json.loads(g.read)) + "How are you, %s!" % event['name']
    except Exception as e:
        return {'error': str(e)}
