import tornado.web

import handlers.base

class FlicksHandler(handlers.base.BaseHandler):

    @tornado.web.authenticated
    def get(self):
    	user = self.get_current_user()
    	flicks = user.flicks
        self.render("flicks.html", user=user, flicks = flicks)


class FlicksCreateHandler(handlers.base.BaseHandler):

    @tornado.web.authenticated
    def get(self):

        # TODO: this will be the form to manually create a flick.  we will try to auto set it to the given movie_id

        movie_id = self.valid("movie_id", required=False)
        
        self.write("movie_id: %s" % movie_id)
