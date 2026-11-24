import http.server
import socketserver
import os
import sys

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Serve static files if they exist
        path = self.translate_path(self.path)
        if not os.path.exists(path) or os.path.isdir(path):
            # Check if this is an SPA route like /blog or /blog/something or /about
            if not self.path.startswith('/assets') and not '.' in os.path.basename(self.path):
                self.path = '/index.html'
        return super().do_GET()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == '__main__':
    with ThreadedHTTPServer(('0.0.0.0', PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        sys.stdout.flush()
        httpd.serve_forever()
