from base_2048 import *
import SimpleHTTPServer, BaseHTTPServer, shutil, json


class HTTPServer2048(BaseHTTPServer.HTTPServer):
    def __init__(self, board):
        BaseHTTPServer.HTTPServer.__init__(self, ('', 3241), Handler2048)
        self.board = board
        board.spawn()

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
            response = json.dumps(data) + "\n"
            self.send_response(200, "OKAY")
            self.send_header("Content-Type","application/json")
            self.send_header("Content-Length", len(response))
            self.end_headers()
            self.wfile.write(response)
        except Exception, e:
            print e
            self.wfile.write("Server error")

    def send_data(self):
        raw = self.server.board._board
        flat = [2**x if x > 0 else 0 for y in raw for x in y]
        self.send_json(flat)

    def do_GET(self):
        if self.path == "/":
            self.send_file("index.html")
        elif self.path == "/main.js":
            self.send_file("main.js")
        elif self.path == "/data.json":
            self.send_data()
        elif self.path == "/d3.v3.min.js":
            self.send_file("d3.v3.min.js")
        else:
            self.send_response(400, "BAD REQUEST")
            self.end_headers()
            self.wfile.write("Unknown request")

    def do_POST(self):
        try:
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            body = json.loads(post_body)
            if "input" in body and body["input"] in ["w","a","s","d"]:
                print "Got input: " + body["input"]
                self.server.board.step(body["input"])
            if "restart" in body:
                print "Restarting"
                self.server.board = Board()
                self.server.board.spawn()
            if "auto" in body:
                print "Automatic move: ",
                self.server.board.auto()
            self.send_data()
        except Exception, e:
            print e
            self.send_response(400, "BAD REQUEST")
            self.end_headers()
            self.wfile.write("Invalid request")


if __name__ == "__main__":
    httpd = HTTPServer2048(Board())
    httpd.serve_forever()