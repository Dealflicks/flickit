import tornado.web

import handlers.base


class HomeHandler(handlers.base.BaseHandler):

    def get(self):
   
        self.render("home.html")



