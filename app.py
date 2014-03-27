# encoding: utf-8

import jinja2
from urlparse import parse_qs
import cgi
from StringIO import StringIO

def app(environ, start_response):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)

    query = parse_qs(environ['QUERY_STRING']).items()
    args = {key : val[0] for key, val in query}

    if environ['REQUEST_METHOD'] == 'POST':
        headers = {
                    'content-type':environ['CONTENT_TYPE'],
                    'content-length':environ['CONTENT_LENGTH']
                  }

        if "multipart/form-data" in environ['CONTENT_TYPE']:
            cLen = int(environ['CONTENT_LENGTH'])
            data = environ['wsgi.input'].read(cLen)
            environ['wsgi.input'] = StringIO(data)

        form = cgi.FieldStorage(fp=environ['wsgi.input'],
                                headers=headers, environ=environ)
        args.update({key : form[key].value for key in form.keys()})

    path = environ['PATH_INFO']
    args['path'] = path

    if path in pages:
        status = '200 OK'
        response_headers, data = pages[path](env, **args)

    else:
        status = '404 Not Found'
        response_headers, data = error(env, **args)

    start_response(status, response_headers)
    return data

### Paths

def index(env, **kwargs):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    template = env.get_template('index.html')
    data = [template.render(kwargs).encode('utf-8')]
    return (response_headers, data)

def content(env, **kwargs):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    template = env.get_template('content.html')
    data = [template.render(kwargs).encode('utf-8')]
    return (response_headers, data)

def file(env, **kwargs):
    kwargs['path'] = '/assets/what.txt'
    return serveFile(env, **kwargs)

def image(env, **kwargs):
    kwargs['path'] = '/assets/catstache.jpeg'
    return serveImage(env, **kwargs)

def css(env, **kwargs):
    return serveCSS(env, **kwargs)

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

### Serving

def serveImage(env, **kwargs):
    response_headers = [('Content-type', 'image/jpeg')]
    data = openFile("."+kwargs['path'])
    return (response_headers, data)

def serveFile(env, **kwargs):
    response_headers = [('Content-type', 'text/plain; charset="UTF-8"')]
    data = openFile("."+kwargs['path'])
    return (response_headers, data)

def serveCSS(env, **kwargs):
    response_headers = [('Content-type', 'text/css; charset="UTF-8"')]
    data = openFile("./assets/default.css")
    return (response_headers, data)

### Helpers

def openFile(fname):
    fp = open(fname, 'rb')
    data = [fp.read()]
    fp.close()
    return data

def make_app():
    return app


pages = {
        '/'        :  index,
        '/content' :  content,
        '/file'    :  file,
        '/image'   :  image,
        '/submit'  :  submit,
        '/css'     :  css,

        '/assets/what.txt' : serveFile,
        '/assets/catstache.jpeg' : serveImage,
        '/assets/images/bg1.jpg' : serveImage,
        '/assets/images/bg2.jpg' : serveImage,
        '/assets/images/db1.gif' : serveImage,
        '/assets/images/db2.gif' : serveImage,
        '/assets/images/border1.gif' : serveImage,
        '/assets/images/border2.gif' : serveImage,
        '/assets/images/boxbg.gif' : serveImage,
        '/assets/images/buttonbg.gif' : serveImage,
        '/assets/images/hdrpic.jpg' : serveImage,
        '/assets/images/icon-printerfriendly.gif' : serveImage,
        '/assets/images/icon-comments.gif' : serveImage,
        '/assets/images/icon-more.gif' : serveImage,
        '/assets/images/menuactive.gif' : serveImage,
        '/assets/images/menubg.gif' : serveImage,
        '/assets/images/pic1.jpg' : serveImage,
        '/assets/images/pic2.jpg' : serveImage,
        '/assets/images/pic3.jpg' : serveImage,
        '/assets/images/topbg.gif' : serveImage,
        '/favicon.ico' : serveImage,

       }
