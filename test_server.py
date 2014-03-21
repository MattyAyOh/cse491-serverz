import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r

        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

expected_OK = 'HTTP/1.0 200 OK\r\n'
expected_NOT_FOUND = 'HTTP/1.0 404 Not Found\r\n'

def test_handle_connection_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80, "myapp")
    assert conn.sent[:len(expected_OK)] == expected_OK, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80, "myapp")
    assert conn.sent[:len(expected_OK)] == expected_OK, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80, "myapp")
    assert conn.sent[:len(expected_OK)] == expected_OK, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80, "myapp")
    assert conn.sent[:len(expected_OK)] == expected_OK, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_404():
    conn = FakeConnection("GET /404 HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80, "myapp")
    assert conn.sent[:len(expected_NOT_FOUND)] == expected_NOT_FOUND, 'Got: %s' % (repr(conn.sent),)

def test_submit_get():
    conn = FakeConnection("GET /submit?firstname=Matt&lastname=Ao \
                           HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80, "myapp")
    assert conn.sent[:len(expected_OK)] == expected_OK, 'Got: %s' % (repr(conn.sent),)

def test_submit_post_urlencoded():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                           "Content-Length: 26\r\n" + \
                           "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
                           "firstname=Matt&lastname=Ao\r\n")
    server.handle_connection(conn, 80, "myapp")
    assert conn.sent[:len(expected_OK)] == expected_OK, 'Got: %s' % (repr(conn.sent),)

def test_submit_post_multipart():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                          "Content-Length: 266\r\n" + \
                          "Content-Type: multipart/form-data; " + \
                          "boundary=08a549bba7a34b5eacdd8e804a00e392\r\n\r\n" + \
                          "--08a549bba7a34b5eacdd8e804a00e392\r\n" + \
                          "Content-Disposition: form-data; name=\"lastname\";" + \
                          " filename=\"lastname\"\r\n\r\n" + \
                          "Ao\r\n" + \
                          "--08a549bba7a34b5eacdd8e804a00e392\r\n" + \
                          "Content-Disposition: form-data; name=\"firstname\";" + \
                          " filename=\"firstname\"\r\n\r\n" + \
                          "Matt\r\n" + \
                          "--08a549bba7a34b5eacdd8e804a00e392--\r\n")
    server.handle_connection(conn, 80, "myapp")
    assert conn.sent[:len(expected_OK)] == expected_OK, 'Got: %s' % (repr(conn.sent),)

def test_submit_post_404():
    conn = FakeConnection("POST /jinkies HTTP/1.0\r\n" + \
                          "Content-Length: 0\r\n" + \
                          "Content-Type: application/x-www-form-urlencoded\r\n\r\n")
    server.handle_connection(conn, 80, "myapp")
    assert conn.sent[:len(expected_NOT_FOUND)] == expected_NOT_FOUND, 'Got: %s' % (repr(conn.sent),)
