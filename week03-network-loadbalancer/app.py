import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERVER_ID = os.getenv("SERVER_ID", "unknown-backend")
PORT = int(os.getenv("PORT", "3000"))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path not in ("/", "/healthz"):
            self.send_json({"error": "Not found", "server": SERVER_ID}, 404)
            return
        self.send_json({"status": "ok", "server": SERVER_ID, "path": path}, 200)

    def send_json(self, data, status):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(f"Starting {SERVER_ID} on port {PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
