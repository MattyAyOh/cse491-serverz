# encoding: utf-8

import jinja2
from urlparse import parse_qs
import cgi
from StringIO import StringIO

def index(env, **kwargs):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    kwargs['img'] = "./assets/catstache.jpeg"
    template = env.get_template('index.html')
    data = [template.render(kwargs).encode('utf-8')]
    return (response_headers, data)

def content(env, **kwargs):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    template = env.get_template('content.html')
    data = [template.render(kwargs).encode('utf-8')]
    return (response_headers, data)

def file(env, **kwargs):
    return serveFile(env, **kwargs)

def image(env, **kwargs):
    return serveImage(env, **kwargs)

def submit(env, **kwargs):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    template = env.get_template('submit.html')
    data = [template.render(kwargs).encode('utf-8')]
    return (response_headers, data)

def error(env, **kwargs):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    template = env.get_template('404.html')
    data = [template.render(kwargs).encode('utf-8')]
    return (response_headers, data)

def app(environ, start_response):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]

    pages["/assets/catstache.jpeg"] = serveImage;
    pages["/assets/what.txt"] = serveFile;

    query = parse_qs(environ['QUERY_STRING']).items()
    args = {key : val[0] for key, val in query}

    if environ['REQUEST_METHOD'] == 'POST':
        headers = {
                    'content-type':environ['CONTENT_TYPE'], \
                    'content-length':environ['CONTENT_LENGTH']
                  }

        if "multipart/form-data" in environ['CONTENT_TYPE']:
            cLen = int(environ['CONTENT_LENGTH'])
            data = environ['wsgi.input'].read(cLen)
            environ['wsgi.input'] = StringIO(data)

        form = cgi.FieldStorage(fp=environ['wsgi.input'], \
                                headers=headers, environ=environ)
        args.update({key : form[key].value for key in form.keys()})


    if environ['PATH_INFO'] in pages:
        status = '200 OK'
        path = environ['PATH_INFO']
    else:
        status = '404 Not Found'
        path = '404'

    args['path'] = path
    response_headers, data = pages[path](env, **args)

    start_response(status, response_headers)
    return data

def serveImage(env, **kwargs):
    response_headers = [('Content-type', 'image/jpeg')]
    data = openFile("./assets/catstache.jpeg")
    return (response_headers, data)

def serveFile(env, **kwargs):
    response_headers = [('Content-type', 'text/plain; charset="UTF-8"')]
    data = openFile("./assets/what.txt")
    return (response_headers, data)

def openFile(fname):
    fp = open(fname, 'rb')
    data = [fp.read()]
    fp.close()
    return data

def make_app():
    return app


pages = {
        '/'        :  index,   \
        '/content' :  content, \
        '/file'    :  file,    \
        '/image'   :  image,   \
        '/submit'  :  submit,  \
        '404'      :  error,   \
       }
