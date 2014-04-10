from apps import *

def get_wsgi_app(quotes_file, files_path):
    return QuotesApp(quotes_file, files_path)
