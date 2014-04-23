#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import socket
from urlparse import urlparse, parse_qs
import time
from StringIO import StringIO
from wsgiref.validate import validator
from sys import stderr
from argparse import ArgumentParser

# from quixote.demo import create_publisher
# from quixote.demo.mini_demo import create_publisher
# from quixote.demo.altdemo import create_publisher


def main():
    args = ArgumentParser(description='Set up WSGI server')
    args.add_argument('-A', metavar='App', type=str, nargs=1, \
                            default='myapp', \
                            choices=['myapp', 'image', 'altdemo', 'quotes',
                            'chat', 'cookie'], \
                            dest='app')
    args.add_argument('-p', metavar='Port', type=int, nargs=1, \
                            default=-1, dest='p')
    argv = args.parse_args()


    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.getfqdn() # Get local machine name
    port = argv.p[0] if argv.p != -1 else 9999
    s.bind((host, port))

    print 'http://%s:%d/' % (host, port)
    s.listen(5)

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c, port, argv.app[0])

def handle_connection(conn, port, app):
    headers = {}
    headers_string = ''
    env={}

    while headers_string[-4:] != '\r\n\r\n':
        headers_string += conn.recv(1)

    initLine, headerData = headers_string.split('\r\n', 1)

    init_list = initLine.split(' ')
    requestType = init_list[0]

    url = urlparse(init_list[1])
    path = url[2]
    query = url[4]

    headers_list = headers_string.split('\r\n')[1:]

    for line in headerData.split('\r\n')[:-2]:
        key, val = line.split(': ', 1)
        headers[key.lower()] = val

    env['REQUEST_METHOD'] = 'GET'
    env['PATH_INFO'] = path
    env['QUERY_STRING'] = query
    env['CONTENT_TYPE'] = 'text/html'
    env['CONTENT_LENGTH'] = str(0)
    env['SCRIPT_NAME'] = ''
    env['SERVER_NAME'] = socket.getfqdn()
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
        env['CONTENT_LENGTH'] = str(headers['content-length'])
        try:
            env['CONTENT_TYPE'] = headers['content-type']
        except:
            pass

        print "CONTENTLENGTH!!!"
        print env['CONTENT_LENGTH']
        content_length = int(headers['content-length'])

        # !!! On Arctic, this drops data
        # content = conn.recv(content_length)

        while len(content) < content_length:
            content += conn.recv(1)

    env['wsgi.input'] = StringIO(content)

    if app == 'altdemo':
        import quixote
        from quixote.demo.altdemo import create_publisher
        try:
            p = create_publisher()
        except RuntimeError:
            pass
        wsgi = quixote.get_wsgi_app()

    elif app == 'image':
        import quixote
        import imageapp
        from imageapp import create_publisher
        try:
            p = create_publisher()
            imageapp.setup()
        except RuntimeError:
            pass

        wsgi = quixote.get_wsgi_app()

    elif app == "quotes":
        import quotes
        wsgi = quotes.get_wsgi_app('./quotes/quotes.txt', './quotes/html')

    elif app == "chat":
        import chat
        wsgi = chat.get_wsgi_app('./chat/html')

    elif app == "cookie":
        import cookieapp
        wsgi = cookieapp.wsgi_app


    else:
        from app import make_app
        wsgi = make_app()

    wsgi = validator(wsgi)
    result = wsgi(env, start_response)


    for data in result:
        conn.send(data)

    result.close()
    conn.close()

if __name__ == '__main__':
    main()
