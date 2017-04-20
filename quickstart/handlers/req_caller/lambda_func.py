import requests
import sys
import json
import os

def handler(conn, event):
    try:
	payload = json.dumps({"name": "GreenT"})
        r = requests.post("http://172.17.0.1:8081/runLambda/hello", data=payload)
        return str(r.status_code) + str(r.content) + "How are you, %s!" % event['name']
        #return "How are you, %s!" % event['name']
    except Exception as e:
        return {'error': str(e)}
