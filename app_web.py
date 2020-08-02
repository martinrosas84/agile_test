from tornado import concurrent, gen
import tornado.web
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line
from controller.handlers import MainHandler
from model.cache import DbConnection

class WebApplication(tornado.web.Application):

    executor = concurrent.futures.ThreadPoolExecutor(5)

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True)
        #IOLoop.current().run_in_executor(self.executor, self.receive_progress)
        self.db = DbConnection()

    def receive_progress(self):
        while True:
            print("something")

if __name__ == "__main__":
    app = WebApplication()
    parse_command_line()
    app.listen(8888)
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.instance().stop()