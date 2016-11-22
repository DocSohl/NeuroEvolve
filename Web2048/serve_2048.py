from base_2048 import *
import SimpleHTTPServer, BaseHTTPServer, shutil, json


class HTTPServer2048(BaseHTTPServer.HTTPServer):
    def __init__(self, board):
        BaseHTTPServer.HTTPServer.__init__(self, ('', 3241), Handler2048)
        self.board = board

class Handler2048(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def send_file(self, filename):
        try:
            self.send_response(200, "OKAY")
            self.end_headers()
            shutil.copyfileobj(open(filename, 'r'), self.wfile)
        except Exception, e:
            print e
            self.wfile.write("Server error")

    def send_json(self, data):
        try:
            self.send_response(200, "OKAY")
            self.end_headers()
            self.wfile.write(json.dumps(data) + "\n")
        except Exception, e:
            print e
            self.wfile.write("Server error")

    def send_data(self):
        self.send_json(self.board._board)

    def do_GET(self):
        if self.path == "/":
            self.send_file("index.html")
        if self.path == "/main.js":
            self.send_file("main.js")
        if self.path == "/data.json":
            self.send_data()
        else:
            self.send_response(200, "OKAY")
            self.end_headers()
            self.wfile.write("Unknown request")

    def do_POST(self):
        pass


if __name__ == "__main__":
    httpd = HTTPServer2048(Board())
    httpd.serve_forever()