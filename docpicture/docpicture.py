


import threading
import BaseHTTPServer
import httplib
import webbrowser

port = 8000


DOCTYPE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html
    PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:svg="http://www.w3.org/2000/svg">"""

END_DOCUMENT = "</html>"

class Element(object):
    '''Prototype from which all the svg elements are derived.

       By design, this enables all elements to automatically give a
       text representation of themselves.'''

    def __init__(self, tag, **attributes):
        '''A basic definition that will be replaced by the specific
           one required by any element.'''
        self.open_tag = "<svg:%s" % tag
        self.tag = tag
        self.sub_elements = []
        if attributes is not None:
            self.attributes = attributes
        else:
            self.attributes = {}

    def __repr__(self):
        attrib = [self.open_tag]
        for att in self.attributes:
            if att != 'text':
                attrib.append(' %s="%s"' % (att, self.attributes[att]))
        if 'text' in self.attributes:
            attrib.append(">\n  %s\n</svg:text>\n" % self.attributes['text'])
        elif self.sub_elements:
            attrib.append(">\n")
            for elem in self.sub_elements:
                attrib.append("  %s" % elem)
            attrib.append("</svg:%s>\n" % self.tag)
        else:
            attrib.append("/>\n")
        return ''.join(attrib)

    def append(self, other):
        self.sub_elements.append(other)


svg_test = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:svg="http://www.w3.org/2000/svg">
  <head>
    <title>SVG embedded inline in XHTML</title>
  </head>
  <body>

    <h1>SVG embedded inline in XHTML</h1>

    <svg:svg width="300px" height="200px">
      <svg:circle cx="150px" cy="100px" r="50px" fill="%s"
                             stroke="#000000" stroke-width="5px"/>
    </svg:svg>

  </body>
</html>
"""
position = ["#330000", "#660000", "#990000",  "#cc0000", "#ff0000"]
index = 0
class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        global index
        self.send_response(200)
        self.send_header('Content-type', 'application/xhtml+xml')
        self.end_headers()
        self.wfile.write(svg_test% position[index % 5])
        index += 1

    def do_QUIT (self):
        """send 200 OK response, and set server.stop to True"""
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    def log_message(self, *args):
        ''' will suppress the usual output'''
        return

class StoppableHttpServer(BaseHTTPServer.HTTPServer):
    """http server that reacts to self.stop flag"""

    def serve_forever (self):
        """Handle one request at a time until stopped."""
        self.stop = False
        while not self.stop:
            self.handle_request()

class TestThread(threading.Thread):
    def run(self):
        server = StoppableHttpServer(('',port), WebRequestHandler)
        webbrowser.open("http://127.0.0.1:%s"%port)
        server.serve_forever()

def stop_server(port):
    """send QUIT request to http server running on localhost:<port>"""
    conn = httplib.HTTPConnection("localhost:%d" % port)
    conn.request("QUIT", "/")
    conn.getresponse()



if __name__ == '__main__':
    import time
    print "Try reloading the page from the Web Browser until the server stops."
    test_thread = TestThread()
    test_thread.start()

    for i in range(10):
        print i
        time.sleep(1)

    stop_server(port)
    print "Done!"
