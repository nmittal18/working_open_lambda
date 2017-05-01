import sys
import json
import os
import string
import time
import random
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
	k = event.get('num_keys',1)
	d = event.get('depth', 1)
	l = event.get('value_len', 1)
	i = event.get('iterations', 100)
	
	fd = open("curl_latency_run_" + str(l) + ".txt", 'wb')
	f = open("curl_output_" + str(l) + ".txt", 'wb')
	data = random_dict(num_keys=k, depth=d, value_len=l)
	payload = json.dumps(data)
	minTime = sys.maxsize
	totalTime = 0
	for _ in range(i):
		start = time.time()
		call(["curl", "-v", "-0", "http://172.17.0.1:8080/runLambda/hello", "-d", payload ], stdout=f, stderr=f)
		end = time.time()
		elapsed = end - start
		totalTime = totalTime + elapsed
		if minTime > elapsed:
			minTime = elapsed
		fd.write("Time elapsed =" + str(elapsed)+ "\n")
        #return str(r.status_code) + str(r.content) + "How are you, %s!" % event['name'] + str(elapsed)+ str(data)
	avgTime = totalTime/i
	fd.write("Average Time =" + str(avgTime)+ "\n")
	fd.write("minTime =" + str(minTime)+ "\n")
	fd.close()
	f.close()
        return "How are you, %s!" % event['name']
    except Exception as e:
        return {'error': str(e)}
