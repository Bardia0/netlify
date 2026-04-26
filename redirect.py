from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import urllib.parse

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL and query parameters
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        # Get the 'u' parameter
        target_urls = query_params.get('u', [])
        
        if not target_urls:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Missing 'u' parameter. Usage: ?u=http://127.0.0.1:port/path")
            return
        
        target_url = unquote(target_urls[0])
        
        # Security check: only allow redirects to 127.0.0.1 or localhost
        if target_url.startswith('http://127.0.0.1') or target_url.startswith('https://127.0.0.1') or \
           target_url.startswith('http://localhost') or target_url.startswith('https://localhost'):
            
            # Send redirect response
            self.send_response(302)
            self.send_header('Location', target_url)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Optional: print to console
            print(f"Redirecting to: {target_url}")
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Only redirects to 127.0.0.1 or localhost are allowed")
    
    def log_message(self, format, *args):
        # Optional: customize logging
        print(f"{self.address_string()} - {format % args}")

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RedirectHandler)
    print(f"Server running on port {port}")
    print(f"Usage: http://localhost:{port}/?u=http://127.0.0.1:3000/path")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server(8080)
