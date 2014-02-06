#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import socket
import urlparse
import time

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000,9000)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port

        handle_connection(c)

def handle_connection(conn):
    requestInfo = conn.recv(1024)
    print requestInfo
    requestSplit = requestInfo.split('\r\n')[0].split(' ')
    requestType = requestSplit[0]

    try:
        parsed_url = urlparse.urlparse(requestSplit[1])
        path = parsed_url[2]
    except:
        path = "/404"

    if requestType == "GET":
        if path == '/':
            handle_index(conn)
        elif path == '/content':
            handle_content(conn)
        elif path == '/file':
            handle_file(conn)
        elif path == '/image':
            handle_image(conn)
        elif path == '/submit':
            handle_submit(conn,parsed_url[4])
        else:
            handle_fail(conn)

    elif requestType == "POST":
        if path == '/':
            handle_index(conn)
        elif path == '/submit':
            handle_submit(conn,requestInfo.split('\r\n')[-1])

    else:
        print "ERROR: Invalid Request Made"

    conn.close()

def handle_index(conn, args):
    conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            "<a href='/content'>Content</a><br>" + \
            "<a href='/file'>File</a><br>" + \
            "<a href='/image'>Image</a><br><br>" + \
            "<p><u>Form Submission via GET</u></p>"
            "<form action='/submit' method='GET'>\n" + \
            "<p>first name: <input type='text' name='firstname'></p>\n" + \
            "<p>last name: <input type='text' name='lastname'></p>\n" + \
            "<p><input type='submit' value='Submit'>\n\n" + \
            "</form></p>" + \
            "<p><u>Form Submission via POST</u></p>"
            "<form action='/submit' method='POST'>\n" + \
            "<p>first name: <input type='text' name='firstname'></p>\n" + \
            "<p>last name: <input type='text' name='lastname'></p>\n" + \
            "<p><input type='submit' value='Submit'>\n\n" + \
            "</form></p>")

def handle_submit(conn, args):
    args = args.split("&")

    firstname = args[0].split("=")[1]
    lastname = args[1].split("=")[1]

    conn.send('HTTP/1.0 200 OK\r\n' + \
              'Content-type: text/html\r\n' + \
              '\r\n' + \
              "Hello Mr. %s %s." % (firstname, lastname))


def handle_content(conn, args):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Here\'s Some Content</h1>')
    conn.send('This is MattyAyOh\'s Web server.')

def handle_file(conn, args):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Here\'s a File</h1>')
    conn.send('This is MattyAyOh\'s Web server.')

def handle_image(conn, args):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Here\'s an Image</h1>')
    conn.send('This is MattyAyOh\'s Web server.')

def handle_fail(conn, args):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>You made a bad request :(</h1>')
    conn.send('This is MattyAyOh\'s Web server.')

if __name__ == '__main__':
    main()
