# image handling API

class Image:
    filename = ''
    data = ''
    comments = []
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        self.comments = []

    def add_comment(self, comment):
        self.comments.append(comment)

    def get_comments(self):
        return self.comments

images = {}

def add_image(filename, data):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0

    image = Image(filename, data)
    images[image_num] = image
    return image_num

def get_image(num):
    return images[num]

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num]
