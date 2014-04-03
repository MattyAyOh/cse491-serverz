from apps import *

def get_wsgi_app(files_path):
    return ChatApp(files_path)
