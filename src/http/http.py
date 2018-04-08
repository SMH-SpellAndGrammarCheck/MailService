#!/usr/bin/env python
# Taken from https://gist.github.com/bradmontgomery/2219997#file-dummy-web-server-py
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from subprocess import call

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        doc = "When issuing a POST request, add a header 'email' containing the "
            + "email address to which the message should be send. The message "
            + "content is read from the POST data."
        self.wfile.write("<html><body><h1>Please issue a POST request!</h1>"
            + doc + "</body></html>")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

    def sendEmail(email_address, content):
        subject = 'Your spelling and grammar check is finished'
        call(['../mail/mail.py',
            '-T', email_address,
            '-B', content,
            '-S', subject
        ])

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
