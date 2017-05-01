# See ipc_call
# This bench does the following:
#       1) Open IPC channel
#       2) Wait for message from call side
#       3) Send Ack
#       4) Exit

from subprocess import call
from posix_ipc import *
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


def handler(conn, event):
    try:
      l = event.get('value_len', 1)
      data = random_dict(num_keys=1, depth=1, value_len=l)
      tmp = pickle.dumps(data)
      mq = MessageQueue("/mytest", flags=O_CREAT, mode=0600, max_messages = 8, max_message_size=len(tmp.encode('utf-8')))
      mq.receive() # Get message from ipc_call
      mq.send("Ack")   # Ack
      mq.close()
      return "Done"
    except Exception as e:
        return {'error': str(e)} 
