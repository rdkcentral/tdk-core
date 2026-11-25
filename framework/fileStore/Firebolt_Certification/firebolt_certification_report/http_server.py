##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2026 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

import http.server
from html import escape
import socketserver
import json
import os
import threading
from urllib.parse import urlparse, unquote, quote

# Set the directory you want to serve files from. The app uploads the JSON, HTML and Excel reports here.
directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
# Each report format is stored in its own sub directory: reports/json, reports/html, reports/xlsx.
FORMATS = ("json", "html", "xlsx")


def format_dir(fmt):
    # Created on demand so uploads and the listing keep working if the reports folder is deleted while running.
    path = os.path.join(directory, fmt)
    os.makedirs(path, exist_ok=True)
    return path


for fmt in FORMATS:
    format_dir(fmt)


def format_of(filename):
    ext = os.path.splitext(filename)[1].lstrip(".").lower()
    return ext if ext in FORMATS else None


def find_report(filename):
    fmt = format_of(filename)
    return os.path.join(format_dir(fmt), filename) if fmt else None


SERVICE_NAME = "firebolt-certification-report"
PORT = int(os.environ.get("FIREBOLT_CERTIFICATION_REPORT_PORT", "8090"))


MAX_UPLOAD_BYTES = int(os.environ.get("FIREBOLT_CERTIFICATION_REPORT_MAX_UPLOAD_BYTES", str(100 * 1024 * 1024)))
REQUEST_TIMEOUT = float(os.environ.get("FIREBOLT_CERTIFICATION_REPORT_REQUEST_TIMEOUT", "30"))
CHUNK_SIZE = 64 * 1024


class MyHandler(http.server.SimpleHTTPRequestHandler):
    # Socket read/write timeout so a stalled client cannot hold a handler forever.
    timeout = REQUEST_TIMEOUT

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type, X-Firebolt-Certification-Report-Name, X-Firebolt-Certification-Report-Format",
        )
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = unquote(parsed_url.path)
        if path == "/health":
            # Lets the app find this server when it had to move off the default port.
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"service": SERVICE_NAME, "port": self.server.server_address[1]}).encode())
        elif path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            sections = ""
            for fmt in FORMATS:
                files = sorted(os.listdir(format_dir(fmt)), reverse=True)
                # Relative links keep working when the server is proxied under a path prefix (e.g. /firebolt-reports/).
                # HTML reports open in the browser; the extra link downloads them like the JSON and Excel reports.
                items = "".join(
                    f"<li><a href='reports/{fmt}/{quote(f)}'>{escape(f)}</a>"
                    + (f" (<a href='reports/{fmt}/{quote(f)}?download=1'>download</a>)" if fmt == "html" else "")
                    + "</li>"
                    for f in files
                )
                sections += f"<h2>{fmt.upper()}</h2><ul>{items}</ul>"
            response = f"<html><body><h1>Firebolt Certification Reports</h1>{sections}</body></html>"
            self.wfile.write(response.encode())
        elif path.startswith("/reports/") and format_of(path):
            report_name = find_report(os.path.basename(path))
            if not report_name or not os.path.isfile(report_name):
                self.send_response(404)
                self.end_headers()
                return
            with open(report_name, "rb") as file:
                self.send_response(200)
                if path.endswith(".html") and "download=1" not in parsed_url.query:
                    self.send_header("Content-type", "text/html")
                else:
                    self.send_header("Content-type", "application/octet-stream")
                    self.send_header("Content-Disposition", f'attachment; filename="{os.path.basename(path)}"')
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_error(404, "Report not found")

    def do_POST(self):
        # Save posted reports under the configured reports directory.
        parsed_url = urlparse(self.path)
        filename = os.path.basename(unquote(parsed_url.path))
        if "refAppExecReport" in filename and format_of(filename):
            filepath = find_report(filename)

            try:
                content_length = int(self.headers.get("Content-Length", ""))
            except ValueError:
                content_length = -1
            if content_length < 0:
                self.send_error(400, "Valid Content-Length required")
                return
            if content_length > MAX_UPLOAD_BYTES:
                self.send_error(413, "Upload too large")
                return

            # Stream to a temp file so a partial or stalled upload never replaces an existing report.
            tmp_path = f"{filepath}.{os.getpid()}.{threading.get_ident()}.part"
            try:
                with open(tmp_path, "wb") as file:
                    remaining = content_length
                    while remaining > 0:
                        chunk = self.rfile.read(min(CHUNK_SIZE, remaining))
                        if not chunk:
                            raise ConnectionError("client closed before sending full body")
                        file.write(chunk)
                        remaining -= len(chunk)
                os.replace(tmp_path, filepath)
            except (OSError, ConnectionError):
                # Includes socket timeouts (TimeoutError is an OSError).
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                self.close_connection = True
                try:
                    self.send_error(408, "Upload incomplete or timed out")
                except OSError:
                    pass
                return

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"<html><body><h1>File {escape(filename)} uploaded successfully.</h1></body></html>".encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Bad Request: expected a refAppExecReport .json, .html or .xlsx file name.")


# Allow quick restarts without waiting for the previous socket to expire.
# Threaded so one slow client cannot block uploads, downloads and health checks.
class ReusableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


MAX_PORT_TRIES = int(os.environ.get("FIREBOLT_CERTIFICATION_REPORT_PORT_TRIES", "20"))


def start_server():
    # If the port is busy, move on to the next one.
    for port in range(PORT, PORT + MAX_PORT_TRIES):
        try:
            return ReusableTCPServer(("0.0.0.0", port), MyHandler), port
        except OSError as error:
            print(f"Port {port} is not available ({error.strerror}); trying {port + 1}")
    raise SystemExit(f"No free port found in range {PORT}-{PORT + MAX_PORT_TRIES - 1}")


httpd, bound_port = start_server()
with httpd:
    print(f"Server started on port {bound_port}")
    print(f"Use reportPublishUrl=http://<this-host>:{bound_port}/")
    httpd.serve_forever()
