import os
import jinja2
import sqlite3
from flask import Flask, request, redirect, url_for, render_template, make_response
from werkzeug.utils import secure_filename

import image

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

############################################################
# Helper Methods
############################################################

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def find_username():
    username = request.cookies.get('username')
    print username
    if not username:
        username = ''
    return username

def authenticate(username, password):
    db = sqlite3.connect('images.sqlite')
    c = db.cursor()
    c.execute('SELECT * FROM user where username=(?)', (username,))
    try:
        username, pwd = c.fetchone()
    except:
        return False
    return pwd == password

def create_database():
    print 'creating database'
    db = sqlite3.connect('images.sqlite')
    db.execute('CREATE TABLE IF NOT EXISTS image_store (i INTEGER PRIMARY KEY, filename VARCHAR(255), \
        owner VARCHAR(30), score INTEGER, image BLOB, \
        FOREIGN KEY (owner) REFERENCES user(username))');
    db.execute('CREATE TABLE IF NOT EXISTS image_comments (i INTEGER PRIMARY KEY, imageId INTEGER, \
     comment TEXT, FOREIGN KEY (imageId) REFERENCES image_store(i))');
    db.execute('CREATE TABLE IF NOT EXISTS user (username VARCHAR(30) PRIMARY KEY, \
        password VARCHAR(30))');
    db.commit()
    db.close()

############################################################
# Serve Methods
############################################################

@app.route('/create_account_receive', methods=['POST'])
def create_account_receive():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    db = sqlite3.connect('images.sqlite')
    c = db.cursor()
    c.execute('SELECT username FROM user WHERE username=(?)', (username,))
    if(c.fetchone() == None):
        db.execute('INSERT INTO user VALUES (?,?)', (username, password))
        db.commit()

    db.close()
    return redirect('./')

@app.route('/upload_receive', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        username = request.cookies.get('username')
        myimage = request.files['file']
        # if myimage and allowed_file(myimage.filename):
        #     filename = secure_filename(myimage.filename)
        #     myimage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return redirect(url_for('uploaded_file',
        #                             filename=filename))

        print 'received file with name:', myimage.filename
        data = myimage.read()
        image.insert_image(myimage.filename, username, data)

    return redirect('./')


@app.route('/login_receive', methods=['POST'])
def login_receive():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    redirect_to_index = redirect('./')
    response = make_response(redirect_to_index)
    if(authenticate(username, password)):
        response.set_cookie('username',value=username)
    return response

@app.route('/logout')
def logout():
    redirect_to_index = redirect('./')
    response = make_response(redirect_to_index)
    response.set_cookie('username',value='')
    return response

@app.route('/jquery')
def jquery():
    return open('jquery-1.11.0.min.js').read()

@app.route('/image_numbers', methods=['GET', 'POST'])
def image_numbers():
    stringList = ",".join(str(x) for x in image.get_image_numbers())
    return stringList

@app.route('/image_raw', methods=['GET'])
def image_raw():
    if request.method == 'GET':
        try:
            num = request.args.get('num')
            if(num == "latest"):
                i = -1
            else:
                i = int(num)
        except:
            i = -1

    img = image.retrieve_image(i)

    filename = img.filename

    response = make_response(img.data)
    if filename.lower() in ('jpg', 'jpeg'):
        response.content_type = 'image/jpeg'
    elif filename.lower() in ('tif',' tiff'):
        response.content_type = 'image/tiff'
    else:
        response.content_type = 'image/png'

    return img.data

@app.route('/get_owner', methods=['POST', 'GET'])
def get_owner():
    if request.method == 'POST':
        try:
            i = int(request.args.get('num'))
        except:
            i = -1
    else:
        i = -1
    return image.get_owner(i)

@app.route('/get_comments', methods=['POST', 'GET'])
def get_comments():
    if request.method == 'POST':
        try:
            i = int(request.args.get('num'))
        except:
            i = -1
    else:
        i = -1

    all_comments = []
    for comment in image.get_comments(i):
        all_comments.append("""
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

@app.route('/add_comment', methods=['POST', 'GET'])
def add_comment():
    if request.method == 'POST':
        try:
            i = int(request.args.get('num'))
        except:
            i = -1
    else:
        i = -1

    try:
        comment = request.form['comment']
    except:
        return

    image.add_comment(i, comment)
    return redirect("/image?num=" + str(i))

@app.route('/get_score', methods=['POST', 'GET'])
def get_score():
    if request.method == 'POST':
        try:
            i = int(request.args.get('num'))
        except:
            i = -1
    else:
        i = -1
    print "I: ", i
    return str(image.get_image_score(i))

@app.route('/increment_score', methods=['POST', 'GET'])
def increment_score():
    if request.method == 'POST':
        try:
            i = int(request.args.get('num'))
        except:
            i = -1
    else:
        i = -1
    image.increment_image_score(i)
    return redirect("/image?num=" + str(i))

@app.route('/decrement_score', methods=['POST', 'GET'])
def decrement_score():
    if request.method == 'POST':
        try:
            i = int(request.args.get('num'))
        except:
            i = -1
    else:
        i = -1
    return redirect("/image?num=" + str(i))

@app.route('/delete_image', methods=['POST', 'GET'])
def delete_image():
    if request.method == 'POST':
        try:
            i = int(request.args.get('num'))
        except:
            i = -1
    else:
        i = -1

    image.delete_image(i)
    return redirect("./")

############################################################
# Serve Pages
############################################################
@app.route('/')
def index():
    return render_template('index.html', username=find_username())

@app.route('/login')
def login():
    return render_template('login.html', username=find_username())

@app.route('/create_account')
def create_account():
    return render_template('create_account.html', username=find_username())

@app.route('/upload')
def upload():
    return render_template('upload.html', username=find_username())

@app.route('/image')
def imageview():
    return render_template('image.html', username=find_username())

@app.route('/image_list')
def image_list():
    return render_template('image_list.html', username=find_username())

############################################################
if __name__ == '__main__':
    create_database()
    app.run(host="0.0.0.0", port=9999)



