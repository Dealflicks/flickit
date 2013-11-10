import tornado.web

import handlers.base

import models.movie
import models.flick

class FlicksHandler(handlers.base.BaseHandler):

    def check_xsrf_token(self):
        pass

    @tornado.web.authenticated
    def get(self):
    	user = self.get_current_user()
    	flicks = user.flicks
        self.render("flicks.html", user=user, flicks = flicks)

    @tornado.web.authenticated
    def post(self):
        movie_id = self.valid("movie_id")

        # need to get user from cookie.
        user = self.get_current_user()

        # TODO: do something if movie doesn't exist
        print movie_id
        movie = models.movie.MovieModel.get_from_mysql_with_id(self.application, movie_id)

        flick = models.flick.FlickModel.get_or_create(self.application, movie.id, user.id)

        has_flicked = False
        if flick:
            has_flicked = True

        movie_dict = { 'poster' : movie.poster, 'dealflicks_url' : movie.dealflicks_url };

        stuff = { 'movie' : movie_dict, 'count' : movie.count, 'has_flicked' : has_flicked}
        
        self.write(stuff)

    
