from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import json
import os
import threading
import time
import httpx

SIGNAL_CLI_PATH = os.environ.get("SIGNAL_CLI_PATH", "signal-cli")
SIGNAL_SERVICE_PHONE = os.environ.get("SIGNAL_SERVICE_PHONE", "")
INTERNAL_API_KEY = os.environ.get("INTERNAL_API_KEY", "change_this_internal_key")
BACKEND_URL = "http://localhost:8000/api/v1/signal/internal/receive"

class SendHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_POST(self):
        if self.path == '/send':
            content_length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(content_length))
            to = body.get('to')
            message = body.get('message')
            if not to or not message:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Paramètres manquants'}).encode())
                return

            cmd = [SIGNAL_CLI_PATH, "-u", SIGNAL_SERVICE_PHONE, "send", "-m", message, to]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                self._set_headers(200)
                self.wfile.write(json.dumps({'status': 'sent'}).encode())
            else:
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': result.stderr}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def log_message(self, format, *args):
        pass

def receive_loop():
    while True:
        try:
            cmd = [SIGNAL_CLI_PATH, "-u", SIGNAL_SERVICE_PHONE, "receive", "--json"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and result.stdout.strip():
                try:
                    messages = json.loads(result.stdout)
                    if isinstance(messages, dict):
                        messages = [messages]
                    for msg in messages:
                        envelope = msg.get('envelope')
                        if envelope and 'dataMessage' in envelope:
                            data = envelope['dataMessage']
                            from_number = envelope.get('source', 'unknown')
                            body = data.get('message')
                            if body:
                                httpx.post(
                                    BACKEND_URL,
                                    json={"from_number": from_number, "body": body},
                                    headers={"X-Internal-Key": INTERNAL_API_KEY},
                                    timeout=5
                                )
                except json.JSONDecodeError:
                    pass
        except Exception:
            pass
        time.sleep(5)

if __name__ == "__main__":
    if not SIGNAL_SERVICE_PHONE:
        raise RuntimeError("La variable d'environnement SIGNAL_SERVICE_PHONE est requise.")

    receiver_thread = threading.Thread(target=receive_loop, daemon=True)
    receiver_thread.start()

    port = 5005
    print(f"Signal bridge en écoute sur le port {port} (service: {SIGNAL_SERVICE_PHONE})")
    HTTPServer(('0.0.0.0', port), SendHandler).serve_forever()