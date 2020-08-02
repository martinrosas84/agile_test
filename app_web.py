from tornado import concurrent, gen
import tornado.web
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line
from controller.handlers import SearchHandler, ReloadTimerHandler
from model.cache import DbConnection
from image_loader import Loader
from tornado.ioloop import PeriodicCallback
from controller.handlers import run_load_images

class WebApplication(tornado.web.Application):

    executor = concurrent.futures.ThreadPoolExecutor(5)

    def __init__(self):
        handlers = [
            (r"/search/(.+)", SearchHandler),
            (r"/reload-timer/([0-9]+)", ReloadTimerHandler),
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True)
        self.db = DbConnection()
        self.reload_images = PeriodicCallback(run_load_images, 120000)

if __name__ == "__main__":
    loader = Loader()
    loader.load_images()
    app = WebApplication()
    app.reload_images.start()
    parse_command_line()
    app.listen(8888)
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.instance().stop()