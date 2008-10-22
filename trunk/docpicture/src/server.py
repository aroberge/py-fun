'''
Stoppable, threadable server

'''

import BaseHTTPServer
import httplib
import socket
import threading
import webbrowser

class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''Request Handler customized to respond to a "QUIT" command and
    which does not log any output'''
    def do_GET(self):
        '''send 200 OK response, and sends a new page'''
        self.send_response(200)
        self.send_header('Content-type', 'application/xhtml+xml')
        self.end_headers()
        self.wfile.write(DOCUMENT)

    def do_QUIT (self):
        """send 200 OK response, and set server.stop to True"""
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    def log_message(self, dummy_format, *dummy_args):
        ''' will suppress the usual output'''
        return

class StoppableHttpServer(BaseHTTPServer.HTTPServer):
    """http server that reacts to self.stop flag"""

    def serve_forever (self):
        """Handle one request at a time until stopped."""
        self.stop = False
        while not self.stop:
            self.handle_request()

class ServerInThread(threading.Thread):
    '''A class designed to start a stoppable HttpServer in a separate thread.'''

    def __init__(self, port=8001):
        '''initializes the port to use for the server and starts the thread'''
        self.port = self.find_port(start=port)
        threading.Thread.__init__(self)

    def run(self):
        '''Method that is called when the start() method of an instance is called'''
        server = StoppableHttpServer(('', self.port), WebRequestHandler)
        webbrowser.open("http://127.0.0.1:%s"%self.port)
        server.serve_forever()

    def find_port(self, start=8001):
        """finds the first free port on 127.0.0.1 starting at start"""
        finalport = None
        testsock = socket.socket()
        testn = start
        while not finalport and (testn < 65536):
            try:
                testsock.bind(('127.0.0.1', testn))
                finalport = testn
            except socket.error:
                testn += 1
        testsock.close()
        return finalport

    def stop_server(self):
        """send QUIT request to http server"""
        conn = httplib.HTTPConnection("localhost:%d" % self.port)
        conn.request("QUIT", "/")
        conn.getresponse()

DOCUMENT = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html
    PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:svg="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink">
  <head>
  </head>
<body>
    This is a test.
    <svg:svg width="300px" height="200px">
      <svg:circle cx="150px" cy="100px" r="50px" fill="#ff0000"
                             stroke="#000000" stroke-width="5px"/>
    </svg:svg>
</body></html>
"""


if __name__ == '__main__':
    import time
    print "Server will be active for 10 seconds."
    threaded_server = ServerInThread()
    threaded_server.start()

    for i in range(1000, 0, -1):
        if not i%100:
            print i,
        time.sleep(0.01)

    threaded_server.stop_server()
    print "Done!"
