from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from cowpy import cow
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    This is a customized server inherited from BaseHTTPRequest Handler class.
    In thie class we re-defined get and post method so that user can ask for
    cow image or json file with different input texts.
    """

    def do_GET(self):
        """
        Here we redefine Get function and handle illegal requests.
        """

        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)

        if parsed_path.path == '/':
            # allow user to get from home directory
            self.send_response(200)
            self.end_headers()

            # to save space, we get the html txt file from reading.
            with open('welcome.html', 'r') as f:
                msg = f.read()

            #return bytes file
            self.wfile.write(msg.encode())
            return

        if parsed_path.path[:10] == '/cow%20msg':
            self.send_response(405)
            self.end_headers()
            return

        # if user input 5000/cow but without any msg info, return bad
        if (parsed_path.path[:4] == '/cow') and ('msg' not in parsed_path.query):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Error: please fill in your message for your cow.')
            return


        if (parsed_path.path[:4] == '/cow') and ('msg' in parsed_path.query):
            self.send_response(200)
            self.end_headers()
            text_msg = parsed_path.query.split("=")[-1]

            # making cow...
            cheese = cow.Moose()
            msg = cheese.milk(text_msg)
            self.wfile.write(msg.encode())
            return

        # for get requesting any other path, return not found.
        self.send_response(404)
        self.end_headers()


    def do_POST(self):
        """
        Here we redefine the post function and handle illegal requests.
        """
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)

        # specify legal format
        if (self.path[:10] == '/cow%20msg'):
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
    Here we initialize the server
    """
    return HTTPServer(
        ('127.0.0.1', 5000),
        SimpleHTTPRequestHandler
    )


def run_forever():
    """
    Here is the main running function that invoke our server.
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
