import tornado.web

import handlers.base

class FlicksHandler(handlers.base.BaseHandler):

    @tornado.web.authenticated
    def get(self):
    	user = self.get_current_user()
    	flicks = user.flicks
        self.render("flicks.html", user=user, flicks = flicks)

    @tornado.web.authenticated
    def post(self):
        movie_id = self.valid("movie_id", required=False)

        # need to get user from cookie.
        user = self.get_current_user()

        # TODO: do something if movie doesn't exist
        print movie_id
        movie = models.movie.MovieModel.get_from_mysql_with_id(self.application, movie_id)

        flick = models.flick.FlickModel.get_or_create(self.application, movie.id, user.id)

        has_flicked = False
        if flick:
            has_flicked = True

        stuff = { 'movie_id' : movie.id, 'count' : movie.count, 'has_flicked' : has_flicked}
        
        self.write("movie_id: %s" % movie_id)

    
