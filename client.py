#!/usr/bin/python3

from random import random, randint
import requests
import signal
import os
import sys
from time import sleep
import json

keep_running = True

def signal_handler(sig, frame):
    global keep_running
    keep_running = False
    print('SIG catched', file=sys.stderr)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

PYAPP_URL = "http://" + os.getenv("PYAPP_HOST") + ":" + os.getenv("PYAPP_PORT")

print("starting to shoot traffic", file=sys.stderr)

while keep_running:
    try:
        ints = [randint(1,200) for _ in range(randint(2,10))]
        if random() > 0.5:
            requests.post(PYAPP_URL + "/multiply", data=json.dumps(ints))
        else:
            requests.post(PYAPP_URL + "/add", data=json.dumps(ints))
    except Exception as e:
        print("failed to make request" + e, file=sys.stderr)
    sleep(random() * 3 + 0.5)