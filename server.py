#!/bin/env python3

# Python 3 server example with timeouts

from datetime import datetime, time, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import environ
from time import sleep

hostName = environ.get("HOSTNAME", "0.0.0.0")
serverPort = environ.get("PORT")
serverPort = 8080 if not serverPort else int(serverPort)
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes(f"<p>Request: {self.path}</p>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
    startTimeout = environ.get("START_TIMEOUT", 5)
    serveTimeout = environ.get("SERVE_TIMEOUT", 30)
    exitTimeout = environ.get("EXIT_TIMEOUT", 600)
    print("SUMMARY:")
    print(f" - sleep {startTimeout}s \t\t\t START_TIMEOUT")
    print(f" - serve content for {serveTimeout}s \t SERVER_TIMEOUT")
    print(f" - sleep {exitTimeout}s, then exit \t EXIT_TIMEOUT\n", flush=True)

    print(f"Sleeping {startTimeout} seconds before serving content", flush=True)
    sleep(startTimeout)

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server running for the next {serveTimeout} seconds, "
          f"http://{hostName}:{serverPort} (HOSTNAME:PORT)", flush=True)

    webServer.timeout = 1  # come back to the while loop every second to evaluate end time
    end = datetime.now() + timedelta(seconds=serveTimeout)
    while datetime.now() < end:
        webServer.handle_request()
    webServer.server_close()
    print("Server stopped.", flush=True)

    print(f"Sleeping {exitTimeout} seconds before exiting", flush=True)
    sleep(exitTimeout)
    print("Exiting")
