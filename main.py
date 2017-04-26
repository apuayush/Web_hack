from tornado.options import options, define, parse_command_line
from tornado.web import RequestHandler, Application, removeslash, UIModule, asynchronous
from tornado.gen import coroutine, Task, engine
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

# other libraries
import os
from pymongo import MongoClient

define('port', default=7777, help='run on the given port', type=int)

db = MongoClient("localhost", 27017)['recker']


class IndexHandler(RequestHandler):
    def get(self):
        all_categories = db.collection.find()
        self.render('index.html', all_categories=all_categories)


class ModuleHandler(UIModule):
    def render(self, category, review, description, image_url, comment):
        return self.render_string("module/div.html",
                                  category=category,
                                  review=review,
                                  description=description,
                                  image_url=image_url,
                                  comment=comment
                                  )


settings = dict(debug=True,
                db=db)

app = Application(
    handlers=[(r'/', IndexHandler)],
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    ui_modules={'ModuleHandler': ModuleHandler},
    **settings)

if __name__ == "__main__":
    parse_command_line()
    HTTPServer(app).listen(options.port)
    IOLoop.instance().start()
