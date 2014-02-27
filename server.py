#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi

from StringIO import StringIO
from app import make_app

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn()     # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port, '\n'
        handle_connection(c)

def handle_connection(conn):
  environ = {}
  request = conn.recv(1)
  
  # This will get all the headers
  while request[-4:] != '\r\n\r\n':
    request += conn.recv(1)

  first_line_of_request_split = request.split('\r\n')[0].split(' ')

  # Path is the second element in the first line of the request
  # separated by whitespace. (Between GET and HTTP/1.1). GET/POST is first.
  http_method = first_line_of_request_split[0]
  environ['REQUEST_METHOD'] = first_line_of_request_split[0]

  try:
    parsed_url = urlparse.urlparse(first_line_of_request_split[1])
    environ['PATH_INFO'] = parsed_url[2]
  except:
    pass

  def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')

  if environ['REQUEST_METHOD'] == 'POST':
    environ = parse_post_request(conn, request, environ)
  elif environ['REQUEST_METHOD'] == 'GET':
    environ['QUERY_STRING'] = parsed_url.query
  wsgi_app = make_app()
  conn.send(wsgi_app(environ, start_response))
  conn.close()

def parse_post_request(conn, request, environ):
  request_split = request.split('\r\n')

  # Headers are separated from the content by '\r\n'
  # which, after the split, is just ''.

  # First line isn't a header, but everything else
  # up to the empty line is. The names are separated
  # from the values by ': '
  for i in range(1,len(request_split) - 2):
      header = request_split[i].split(': ', 1)
      environ[header[0].upper()] = header[1]

  content_length = int(environ['CONTENT-LENGTH'])
  
  content = ''
  for i in range(0,content_length):
      content += conn.recv(1)

  environ['wsgi.input'] = StringIO(content)
  return environ

if __name__ == '__main__':
   main()
