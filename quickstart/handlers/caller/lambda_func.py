import requests
#import sys
import json
from subprocess import call

def handler(conn, event):
    try:
	payload = json.dumps({'name':'Neha'})
	f = open("x", 'w')
	g = open("y", 'w')
        #call(["perf","record", "-e", "syscalls:sys_*", "-e", "net:*", "-e", "skb:*", "-e", "sock:*", "-F", "99", "-a", "-g", "--","curl -X POST localhost:8082/runLambda/hello -d '{}'" ], stdout=f, stderr=g)
        #call(["perf","record", "-e", "cpu-clock","-F", "99", "-a", "-g", "--","curl -X POST http://172.17.0.1:8081/runLambda/hello -d '{}'" ], stdout=f, stderr=g)
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
