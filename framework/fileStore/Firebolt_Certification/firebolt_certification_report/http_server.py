import http.server
import socketserver
import json
import os
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


class MyHandler(http.server.SimpleHTTPRequestHandler):

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
                    f"<li><a href='reports/{fmt}/{quote(f)}'>{f}</a>"
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
            super().do_GET()

    def do_POST(self):
        # Save posted reports under the configured reports directory.
        parsed_url = urlparse(self.path)
        filename = os.path.basename(unquote(parsed_url.path))
        if "refAppExecReport" in filename and format_of(filename):
            filepath = find_report(filename)

            # Read the data from the POST request and save it to the file.
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            with open(filepath, "wb") as file:
                file.write(post_data)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"<html><body><h1>File {filename} uploaded successfully.</h1></body></html>".encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Bad Request: expected a refAppExecReport .json, .html or .xlsx file name.")


# Allow quick restarts without waiting for the previous socket to expire.
class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


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
