import json
import logging

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread

context = None
PRESENCE_FILE_PATH = Path.home() / ".local" / "share" / "safeeyes" / "teamspresence"


def init(ctx, safeeyes_config, plugin_config) -> None:
    global context
    context = ctx
    context["plugin_config"] = plugin_config
    server_thread = Thread(target=run_server, args=(5000,), daemon=True)
    server_thread.start()


def on_pre_break(break_obj) -> bool:
    """Lifecycle method executes before the pre-break period."""
    return _should_skip_break()


def on_start_break(break_obj) -> bool:
    """Lifecycle method executes just before the break."""
    return _should_skip_break()


def _should_skip_break() -> bool:
    presence = PRESENCE_FILE_PATH.read_text()
    setting = f"presence_{presence.replace('-', '_')}"
    if setting not in context["plugin_config"]:
        logging.warning(f"{presence} is not a valid presence status.")
        return False
    if context["plugin_config"][setting]:
        logging.info(f"Teams presence status is {presence}. Skipping break.")
        return True
    logging.info(f"Teams presence status is {presence}. Break allowed.")
    return False


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
        PRESENCE_FILE_PATH.parent.mkdir(exist_ok=True)
        PRESENCE_FILE_PATH.write_text(status)


def run_server(port=5000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    logging.info(f"Starting teams presence httpd on port {port}...")
    httpd.serve_forever()
