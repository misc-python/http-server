from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from cowpy import cow
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    """

    def do_GET(self):
        """
        """

        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)
        # import pdb; pdb.set_trace()
        if parsed_path.path == '/':
            # Query the DB here - Then format your response
            self.send_response(200)
            self.end_headers()
            # self.wfile.write(b'<html><body><h1>hello</h1><body></html>')
            with open('welcome.html', 'r') as f:
                msg = f.read()
            self.wfile.write(bytes(msg.encode()))
            return

        if parsed_path.path[:10] == '/cow%20msg':
            self.send_response(405)
            self.end_headers()
            return

        # import pdb; pdb.set_trace()
        # if user input 5000/cow but without any msg info, return bad
        if (parsed_path.path[:4] == '/cow') and ('msg' not in parsed_path.query):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Error: please fill in your message for your cow.')
            return

        # if 'cow' in parsed_path.path:
        if (parsed_path.path[:4] == '/cow') and ('msg' in parsed_path.query):
            # do some format checking for path

            # assuming we get path = "/cow?msg=text text text text"
            self.send_response(200)
            self.end_headers()
            text_msg = parsed_path.query.split("=")[-1]
            cheese = cow.Moose()
            msg = cheese.milk(text_msg)
            self.wfile.write(msg.encode())
            return

        if parsed_path.path == '/hello':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>hello world!</h1></body></html>')
            return

        self.send_response(404)
        self.end_headers()

    def do_HEAD(self):
        """
        """
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        """
        """
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)
        # import pdb; pdb.set_trace()
        if (self.path[:10] == '/cow%20msg'):
            # do some format checking for path

            # assuming we get path = "/cow?msg=text text text text"
            self.send_response(201)
            self.end_headers()
            text_msg = parsed_path.query.split("=")[-1]
            cheese = cow.Moose()
            msg = cheese.milk(text_msg)
            text_dic = { "content" : msg}
            self.wfile.write(json.dumps(text_dic).encode())
            return

        if (self.path[:8] == '/cow?msg'):
            self.send_response(405)
            self.end_headers()
            return


        if (self.path[:4] == '/cow') or (parsed_path.path == '/'):
            self.send_response(400)
            self.end_headers()
            return

        self.send_response(404)
        self.end_headers()


def create_server():
    """
    """
    return HTTPServer(
        ('127.0.0.1', 5000),  # TODO: Make these ENV Vars
        SimpleHTTPRequestHandler
    )


def run_forever():
    """
    """
    server = create_server()

    try:
        print(f'Starting server on 127.0.0.1:5000')
        server.serve_forever()
    except KeyboardInterrupt as error:
        print('Thanks for running the server. Shutting down...')
        print(error.message)
        server.server_close()  # Politely closes active sockets
        server.shutdown()  # Politely shuts down the server instance


if __name__ == '__main__':
    run_forever()
