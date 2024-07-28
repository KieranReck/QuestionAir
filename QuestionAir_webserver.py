import http.server
import socketserver
from urllib.parse import parse_qs

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print ("MY SERVER: I got a GET request.")
        # set the default webpage when port is accessed at root
        if self.path == '/':
            print ("MY SERVER: The GET request is for the root URL.")
            self.path = 'home.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        print ("MY SERVER: I got a POST request.")
        if self.path == '/data_entry':
            print ("MY SERVER: The POST request is for the /data_entry URL.")

            content_length = int(self.headers['Content-Length'])
            post_data_bytes = self.rfile.read(content_length)
            print ("MY SERVER: The post data I received from the request has following data:\n", post_data_bytes)

            post_data_str = post_data_bytes.decode("UTF-8")
            post_data_dict =parse_qs(post_data_str)
            print ("MY SERVER: I have changed the post data to a dict and here it is:\n", post_data_dict)


            self.path = 'home.html';
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)

# Star the server
my_server.serve_forever()