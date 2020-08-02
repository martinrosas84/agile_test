from tornado.web import RequestHandler
from tornado import concurrent

class BasicHandler(RequestHandler):

    executor = concurrent.futures.ThreadPoolExecutor(10)

class MainHandler(RequestHandler):
    def get(self):
        self.write('ok')