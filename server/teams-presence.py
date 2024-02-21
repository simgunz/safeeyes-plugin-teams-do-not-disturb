from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.add_cors_headers()
        self.end_headers()

    def do_POST(self):
        self.add_cors_headers()
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")

        try:
            data = json.loads(body)
            if "status" in data:
                self.write_status_to_file(data["status"])
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"ok")
            else:
                self.send_error(400, "Missing 'status' in JSON data")
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON data")

    def add_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def write_status_to_file(self, status):
        safeeyes_presence_file = (
            Path.home() / ".local" / "share" / "safeeyes" / "teamspresence"
        )
        safeeyes_presence_file.parent.mkdir(exist_ok=True)
        safeeyes_presence_file.write_text(status)


def run(port=5000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Starting httpd on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
