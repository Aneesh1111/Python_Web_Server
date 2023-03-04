
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from typing import Tuple

# 8000 doesn't mean anything, feel free to change to any other 4 digit number
PORT = 9999


# if you haven't seen this syntax before, it's Python's inheritance,
# and in this case it means MyHandler extends BaseHTTPRequestHandler
class MyHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)  # 200 stands for request succeeded
        self.send_header("Content-type", "text/html")  # informs requests of the Media type
        self.end_headers()

    # entering the localhost url into your browser, you will get an additional /favicon.ico path,
    # so take this into account with testing.
    # this method is where
    def do_GET(self):
        self._set_headers()
        print(self.path)  
        json_string = json.dumps({'standard': 'greeting'})
        self.wfile.write(json_string.encode(encoding='utf_8'))

    def do_POST(self):
        self._set_headers()
        print(self.path)
        # 1. How long was the message?
        length = int(self.headers.get('Content-length', 0))

        # 2. Read the correct amount of data from the request.
        data = self.rfile.read(length).decode()
        print(data)

        # 3. Extract the "message" field from the request data.
        message = 'new ting'#parse_qs(data)["message"][0]
        json_string = json.dumps(data)


def run(server_class=HTTPServer, handler_class=MyHandler, addr="172.26.203.220", port=PORT):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {addr}:{port}")  # f before string allows special formatting
    httpd.serve_forever()


# the next line basically checks if your configurations set this file as the "main" file,
# and if so, run the following code.
# if this code is imported into another project, that means the following code won't run,
# because this file is not the main file.
if __name__ == "__main__":
    thread = threading.Thread(target=run)
    thread.start()
    url = f'http://172.26.203.220:{PORT}/hello'
    request = requests.get(url)  # example of a client side request for data
    print(request.json())
