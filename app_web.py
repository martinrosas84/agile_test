from tornado import concurrent, gen
import tornado.web
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line
from controller.handlers import MainHandler
from model.cache import DbConnection
from image_loader import Loader

class WebApplication(tornado.web.Application):

    executor = concurrent.futures.ThreadPoolExecutor(5)

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True)
        self.db = DbConnection()

if __name__ == "__main__":
    loader = Loader()
    loader.load_images()
    app = WebApplication()
    parse_command_line()
    app.listen(8888)
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.instance().stop()