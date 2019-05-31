from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse
from urlparse import parse_qs

class httpHandler(BaseHTTPRequestHandler):
# Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        # Send the html message
        o = urlparse(self.path)
        query = parse_qs(o.query)
        out = get_handler.get_handler(query)
        self.wfile.write(out)
        return

def make_server(host,port,handler):
    global get_handler
    get_handler = handler
    server = HTTPServer((host, port),httpHandler )
    return server
