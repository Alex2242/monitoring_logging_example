from prometheus_client import start_http_server, Summary, Counter
import random
import time
import signal
import sys
import os
import json
import logging
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Create a metric to track time spent and requests made.
CALLS = Counter('pyapp_called', 'number of calls made to the server', ['method', 'endpoint'])
CALLS.labels('get', '/')
CALLS.labels('post', '/add')
CALLS.labels('post', '/multiply')
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, content_type='application/json', data=None):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()
        if data:
            self.wfile.write(json.dumps(data).encode('utf-8'))
    
    @REQUEST_TIME.time()
    def do_GET(self):
        if self.path == '/':
            CALLS.labels('get', '/').inc()
            self._send_response(200, data={'message': 'Hello, World!'})
            self.log_req("GET", self.path, 200)
        else:
            self._send_response(404, data={'error': 'Not Found'})
            self.log_req("GET", self.path, 404)

    @REQUEST_TIME.time()
    def do_POST(self):
        if self.path == '/add':
            CALLS.labels('post', '/add').inc()
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            ints = json.loads(post_data)
            response_data = {'result': sum(ints)}
            self._send_response(201, data=response_data)
            self.log_req("POST", self.path, 201)

        elif self.path == '/multiply':
            CALLS.labels('post', '/multiply').inc()
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            ints = json.loads(post_data)
            response_data = {'result': sum(ints)}
            self._send_response(201, data=response_data)
            self.log_req("POST", self.path, 201)
        else:
            self._send_response(404, data={'error': 'Not Found'})
            self.log_req("POST", self.path, 404)

    def log_req(self, verb="POST", path="/add", status=200):
        with open(os.getenv('PYAPP_LOG_FILE'), "a") as flog:
            msg_dict = {"http_verb": verb, "path": path, "status": status, "time": int(datetime.now().timestamp())}
            flog.write(json.dumps(msg_dict) + "\n")


if __name__ == '__main__':
    if not os.getenv('PYAPP_LOG_FILE'):
        print("[ERROR] missing env var PYAPP_LOG_FILE", file=sys.stderr)
        sys.exit(1)
    if not os.getenv('PYAPP_PORT'):
        print("[ERROR] missing env var PYAPP_PORT", file=sys.stderr)
        sys.exit(1)

    # Start up the server to expose the metrics.
    start_http_server(8000)

    port = int(os.getenv("PYAPP_PORT"))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Starting httpd server on port {port}...', file=sys.stderr)
    httpd.serve_forever()