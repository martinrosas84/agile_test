from tornado.web import RequestHandler
from tornado import concurrent
from tornado.ioloop import PeriodicCallback
from image_loader import Loader

def run_load_images():
    '''
    Runs the loader
    '''
    loader = Loader()
    loader.load_images()

class SearchHandler(RequestHandler):
    def get(self, term):
        images = self.application.db.search(term)
        self.write({"pictures": self.images_to_json(images)})

    def images_to_json(self, images):
        '''
        Convert the response of the database in a full Json reponse in a one line fashion
        '''
        return [{
            "id": img[0],
            "author": img[1],
            "camera": img[2],
            "tags": img[3],
            "cropped_picture": img[4],
            "full_picture": img[5]
        } for img in images]

class ReloadTimerHandler(RequestHandler):
    def get(self, arg_time):
        time = float(arg_time) * 60000
        self.application.reload_images.stop()
        self.application.reload_images = PeriodicCallback(run_load_images, time)
        self.application.reload_images.start()
        self.write('ok')