import tornado.web

import handlers.base

class FlicksHandler(handlers.base.BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("flicks.html")
