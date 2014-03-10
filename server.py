#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import socket
from urlparse import urlparse, parse_qs
import time
import cgi
from StringIO import StringIO
import jinja2
from wsgiref.validate import validator
from sys import stderr

from app import make_app
import quixote
import imageapp


# from quixote.demo import create_publisher
# from quixote.demo.mini_demo import create_publisher
# from quixote.demo.altdemo import create_publisher
# p = create_publisher()

# imageapp.setup()
# p = imageapp.create_publisher()


def main():
    s = socket.socket()
    host = socket.gethostname() # Get local machine name
    # port = random.randint(8000,9000)
    port = 9998
    s.bind((host, port))

    print 'http://%s:%d/' % (host, port)
    s.listen(5)

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c, port)

def handle_connection(conn, port):

    headers_string = ''
    while headers_string[-4:] != '\r\n\r\n':
        headers_string += conn.recv(1)

    init_list = headers_string.split('\r\n')[0].split(' ')
    requestType = init_list[0]

    url = urlparse(init_list[1])
    path = url[2]
    query = url[4]
    args = parse_qs(query)

    headers = {}
    headers_list = headers_string.split('\r\n')

    for i in range(1,len(headers_list)-2):
        header = headers_list[i].split(': ', 1)
        headers[header[0].lower()] = header[1]

    env={}
    env['REQUEST_METHOD'] = 'GET'
    env['PATH_INFO'] = path
    env['QUERY_STRING'] = query
    env['CONTENT_TYPE'] = 'text/html'
    env['CONTENT_LENGTH'] = str(0)
    env['SCRIPT_NAME'] = ''
    env['SERVER_NAME'] = socket.gethostname()
    env['SERVER_PORT'] = str(port)
    env['wsgi.version'] = (1, 0)
    env['wsgi.errors'] = stderr
    env['wsgi.multithread']  = False
    env['wsgi.multiprocess'] = False
    env['wsgi.run_once']     = False
    env['wsgi.url_scheme'] = 'http'
    env['HTTP_COOKIE'] = headers['cookie'] if 'cookie' in headers.keys() else ''

    def start_response(status, headers_response):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in headers_response:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')

    content=''
    if requestType == "POST":
        env['REQUEST_METHOD'] = 'POST'
        env['CONTENT_LENGTH'] = headers['content-length']
        env['CONTENT_TYPE'] = headers['content-type']

        content_length = int(headers['content-length'])
        content = conn.recv(content_length)

    env['wsgi.input'] = StringIO(content)

    # wsgi = quixote.get_wsgi_app()
    wsgi = make_app()
    wsgi = validator(wsgi)
    result = wsgi(env, start_response)


    for data in result:
        conn.send(data)

    result.close()
    conn.close()

if __name__ == '__main__':
    main()
