from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib3
from urllib.parse import urlparse, parse_qs
import html.parser
hostName = "localhost"
serverPort = 3000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        parse_result = urlparse(self.path)
        dict_result = parse_qs(parse_result.query)
        print(dict_result["objectId"])
        self.send_header('Location','http://localhost:8501')
        self.end_headers()

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")