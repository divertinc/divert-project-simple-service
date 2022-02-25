#!/usr/bin/env python
# Copyright (c) 2022 Divert, Inc.
import logging
import os
import json

from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus


def main():
    server = DvSServer()
    server.serve()


class DvSServer:
    SERVER_VERSION: str = "1.1"
    
    def __init__(self):
        self.server_host: str = os.getenv("HOST") or "127.0.0.1"
        self.server_port: int = os.getenv("PORT") or 8001

    def serve(self):
        logging.info(f"Serving at http://{self.server_host}:{self.server_port}")
        with HTTPServer(server_address=(self.server_host, self.server_port),
                        RequestHandlerClass=DvRequestHandler,
                        ) as httpd:
            httpd.serve_forever(poll_interval=1.0)


class DvRequestHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        content_length = int(self.headers.get("Content-length"))
        request_body = self.rfile.read(content_length)
        request_content = json.loads(bytes.decode(request_body, "utf8"))
        self.log_message(f"REQUEST: {request_content}")
        
        response = {
            "server_version": DvSServer.SERVER_VERSION,
            "message": request_content["message"],
        }
        response_body = bytes(json.dumps(response), "utf8")
        self.log_message(f"RESPONSE: {response}")
        
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)


if __name__ == '__main__':
    main()
