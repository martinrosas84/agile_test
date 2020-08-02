from tornado.web import RequestHandler
from tornado import concurrent

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