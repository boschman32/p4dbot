from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


PORT_NUMBER = 8080

# This class will handles any incoming request from
# the browser


class httpHandler(BaseHTTPRequestHandler):
# Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("Hello World !")
        return
    def do_POST(self):
        if self.path == "/":
            form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
            'CONTENT_TYPE': self.headers['Content-Type'],
            })
            print form
            print "Your name is: %s" % form["name"]
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Thanks %s !" % form["name"])
        return	

    
def make_server(host,port):
	return HTTPServer((host, port), httpHandler)
