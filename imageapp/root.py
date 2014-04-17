import quixote
from quixote.directory import Directory, export, subdir
from quixote.util import StaticFile
import os.path

from . import html, image

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        return html.render('index.html')

    @export(name='jquery')
    def jquery(self):
        return open('jquery-1.11.0.min.js').read()

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(the_file.get_size())

        image.add_image(the_file.base_filename, data)

        return quixote.redirect('./')

    @export(name='upload2')
    def upload2(self):
        return html.render('upload2.html')

    @export(name='upload2_receive')
    def upload2_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(the_file.get_size())

        image.add_image(the_file.base_filename, data)

        return html.render('upload2_received.html')

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_list')
    def image_list(self):
        return html.render('image_list.html')

    @export(name='image_count')
    def image_count(self):
        return len(image.images)

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()
        try:
            img = image.get_image(int(request.form['num']))
        except KeyError:
            img = image.get_latest_image()

        filename = img.filename
        if filename.lower() in ('jpg', 'jpeg'):
            response.set_content_type('image/jpeg')
        elif filename.lower() in ('tif',' tiff'):
            response.set_content_type('image/tiff')
        else: # Default to .png for reasons
            response.set_content_type('image/png')
        return img.data

    @export(name='get_comments')
    def get_comments(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            img = image.get_image(int(request.form['num']))
        except KeyError:
            img = image.get_latest_image()

        all_comments = []
        for comment in img.get_comments():
            print comment
            all_comments.append("""\
    <comment>
     <text>%s</text>
    </comment>
    """ % (comment))

        xml = """
    <?xml version="1.0"?>
    <comments>
    %s
    </comments>
    """ % ("".join(all_comments))

        return xml

    @export(name='add_comment')
    def add_comment(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            img = image.get_image(int(request.form['num']))
        except KeyError:
            img = image.get_latest_image()

        try:
            comment = request.form['comment']
        except:
            return

        img.add_comment(comment)
