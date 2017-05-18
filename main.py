import os.path

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# other libraries
import os
from pymongo import MongoClient

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

db = MongoClient("localhost", 27017)['recker']


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        all_categories = db.collection.find()
        self.render('index.html', all_categories=all_categories, page_title="HOME | Cosmos")


class ModuleHandler(tornado.web.UIModule):
    def render(self, category, review, description, image_url, comment):
        return self.render_string("Module/ui.html",
                                  category=category,
                                  review=review,
                                  description=description,
                                  image_url=image_url,
                                  comment=comment
                                  )


settings = dict(debug=True,
                db=db)

app = tornado.web.Application(
    handlers=[(r'/', IndexHandler)],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    ui_modules={'ModuleHandler': ModuleHandler},
    **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    tornado.httpserver.HTTPServer(app).listen(options.port)
    tornado.ioloop.IOLoop.current().start()
