from http.server import SimpleHTTPRequestHandler, HTTPServer
import base64
import sys

class AuthHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server, username, password):
        self.username = username
        self.password = password
        super().__init__(request, client_address, server)

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Test"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.headers.get('Authorization') is None:
            self.do_AUTHHEAD()
            self.wfile.write(b'no auth header received')
        else:
            encoded_credentials = base64.b64encode(f'{self.username}:{self.password}'.encode()).decode('utf-8')
            if self.headers.get('Authorization') == f'Basic {encoded_credentials}':
                super().do_GET()
            else:
                self.do_AUTHHEAD()
                self.wfile.write(b'not authenticated')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python3 auth2.py <username> <password> <port>")
        sys.exit(1)

    username, password, port = sys.argv[1], sys.argv[2], int(sys.argv[3])

    server_address = ('', port)
    httpd = HTTPServer(server_address, lambda request, client_address, server: AuthHandler(request, client_address, server, username, password))
    print(f'Starting server on port {port}...')
    httpd.serve_forever()
