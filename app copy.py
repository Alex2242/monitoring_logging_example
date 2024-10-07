from prometheus_client import start_http_server, Summary
import random
import time
import signal
import sys
import os
import json
import logging
from datetime import datetime

N = 0

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)
    global N
    N += 1
    with open(os.getenv('PYAPP_LOG_FILE'), "a") as flog:
        msg_dict = {"job_id": N, "processing_duration": t, "time": int(datetime.now().timestamp())}
        flog.write(json.dumps(msg_dict) + "\n")


if __name__ == '__main__':
    if not os.getenv('PYAPP_LOG_FILE'):
        print("[ERROR] missing env var PYAPP_LOG_FILE")
        sys.exit(1)

    logging.info("processing requests")
    print("processing requests")
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    print("processing requests")

    keep_running = True

    def signal_handler(sig, frame):
        global keep_running
        keep_running = False
        print('SIG catched')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while keep_running:
        process_request(5 * random.random())