#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import socket
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
        requestInfo = c.recv(1024)
        requestType = requestInfo.split()[0]

        if requestType == "GET":
            url = requestInfo.split()[1]
            
            if url == '/':
                handle_connection_default(c)
            elif url == '/content':
                handle_connection_content(c)
            elif url == '/file':
                handle_connection_file(c)
            elif url == '/image':
                handle_connection_image(c)
            else:
                handle_connection_fail(c)

        elif requestType == "POST":
                handle_post_connection(c)

        else:
            print "ERROR: Invalid Request Made"
            break

    
def handle_connection_default(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Hello, world.</h1>')
    conn.send('<a href="/content">Content</a><br>')
    conn.send('<a href="/file">File</a><br>')
    conn.send('<a href="/image">Image</a><br>')
    conn.send('This is MattyAyOh\'s Web server.')
    conn.close()

def handle_connection_content(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Here\'s Some Content</h1>')
    conn.send('This is MattyAyOh\'s Web server.')
    conn.close()

def handle_connection_file(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Here\'s a File</h1>')
    conn.send('This is MattyAyOh\'s Web server.')
    conn.close()

def handle_connection_image(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Here\'s an Image</h1>')
    conn.send('This is MattyAyOh\'s Web server.')
    conn.close()

def handle_connection_fail(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>You made a bad request :(</h1>')
    conn.send('This is MattyAyOh\'s Web server.')
    conn.close()

def handle_post_connection(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('Hello, World.  This is a Post Response')
    conn.close()

if __name__ == '__main__':
    main()