import tornado.web

import handlers.base

class FlicksHandler(handlers.base.BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("flicks.html")


class FlicksCreateHandler(handlers.base.BaseHandler):

    @tornado.web.authenticated
    def get(self):

        # TODO: this will be the form to manually create a flick.  we will try to auto set it to the given movie_id

        movie_id = self.valid("movie_id", required=False)
        
        self.write("movie_id: %s" % movie_id)
