from urllib.parse import urljoin
from urllib.request import urlopen
from utils import say_hello, say_bye, modify_text

import http.server

LOCAL_HOST, LISTEN_PORT = '127.0.0.1', 9000
TARGET_HOST = 'https://habrahabr.ru'


class HabraHandler(http.server.BaseHTTPRequestHandler):
    """
    Custom HTTP request handler class.
    """
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        url = urljoin(TARGET_HOST, self.path)

        try:
            modified = modify_text(url)
            self.wfile.write(modified)
        except UnicodeDecodeError:
            self.wfile.write(urlopen(url).read())
        except IndexError:
            self.wfile.write(urlopen(url).read())
        except Exception as exc:
            print('Unexpected error', exc)


def main():
    server_class = http.server.HTTPServer
    httpd = server_class((LOCAL_HOST, LISTEN_PORT), HabraHandler)
    say_hello(LOCAL_HOST, LISTEN_PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    say_bye()


if __name__ == '__main__':
    main()
