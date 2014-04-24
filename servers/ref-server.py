#! /usr/bin/env python
import socket
import random

from wsgiref.simple_server import make_server

from app import make_app

###

the_wsgi_app = make_app()

host = socket.gethostname() # Get local machine name
port = random.randint(8000, 9999)
httpd = make_server('', 9999, the_wsgi_app)
print "Serving at http://%s:%d/..." % (host, port,)
httpd.serve_forever()
