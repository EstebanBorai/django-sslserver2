import os
import ssl
import sys

from django.core.servers.basehttp import WSGIRequestHandler, WSGIServer
from django.core.management.base import CommandError
from django.core.management.commands import runserver
from socket import error as SocketException
from socketserver import ThreadingMixIn
from threading import Thread


class ThreadedWSGIServer(ThreadingMixIn, WSGIServer):
    pass


class WSGIHttpsRequestHandler(WSGIRequestHandler):
    def get_environ(self):
        env = super(WSGIRequestHandler, self).get_environ()
        env["HTTPS"] = "on"

        return env


class HttpsServer(ThreadedWSGIServer):
    """
    Implementation on the HTTPS server
    """

    def __init__(self, address, handler_cls, certificate, key):
        super(HttpsServer, self).__init__(address, handler_cls)

        self.socket = ssl.wrap_socket(
            self.socket,
            certfile=certificate,
            keyfile=key,
            server_side=True,
            ssl_version=ssl.PROTOCOL_TLS,
            cert_reqs=ssl.CERT_NONE,
        )


class HttpServerThread(Thread):
    """Thread for a WSGI Http/s Server"""

    def __init__(self, server, handler):
        Thread.__init__(self)

        self.__server = server
        self.__handler = handler

    def run(self):
        self.__server.set_app(self.__handler)
        self.__server.serve_forever()


class Command(runserver.Command):
    """
    Extension on Django's `runserver` command which spawns a thread running a
    HTTPS server with the provided configuration along with the default
    runserver command.
    """

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument("--certificate", help="Path to SSL certificate file")
        parser.add_argument("--key", help="Path to SSL certificate key")

    def validate(self, certificate_path: str, key_path: str):
        if not os.path.exists(certificate_path) or not os.path.exists(key_path):
            raise CommandError(
                f"Can't find certifiacate/key files. Check files are available on:\n- {certificate_path}\n - {key_path}"
            )

    def inner_run(self, *args, **options):
        ssl_certificate_path = options.get("certificate")
        ssl_key_path = options.get("key")

        self.validate(str(ssl_certificate_path), str(ssl_key_path))
        self.check(display_num_errors=True)

        try:
            server_address = self._raw_ipv6 and "[%s]" % self.addr or self.addr
            http_server_port = int(self.port)
            https_server_port = int(self.port) + 1

            self.stdout.write(
                ("Starting development server at http://%(addr)s:%(port)s/\n")
                % {
                    "addr": server_address,
                    "port": http_server_port,
                }
            )

            self.stdout.write(
                ("Starting development server at https://%(addr)s:%(port)s/\n")
                % {
                    "addr": server_address,
                    "port": https_server_port,
                }
            )

            handler = self.get_handler(*args, **options)
            server = HttpsServer(
                (self.addr, https_server_port),
                WSGIHttpsRequestHandler,
                ssl_certificate_path,
                ssl_key_path,
            )

            https_server_thread = HttpServerThread(server, handler)
            https_server_thread.start()

            self.stdout.write("HTTPS Server Thread spawned")

            runserver.run(
                addr=server_address,
                port=http_server_port,
                wsgi_handler=handler,
                ipv6=False,
                threading=True,
            )

        except SocketException:
            err = sys.exc_info()[1]
            message = str(err)
            self.stderr.write("Error: %s" % message)
            os._exit(1)

        except KeyboardInterrupt:
            self.stdout.write("Shutting down server...")

        except:
            self.stderr.write("An error has ocurred!")

        finally:
            sys.exit(0)
