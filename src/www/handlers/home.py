import tornado.web

import handlers.base
import models.movie

class HomeHandler(handlers.base.BaseHandler):

    def get(self):
		user = self.get_current_user()
		flicks = user.flicks
		golden_movies = models.movie.MovieModel.get_golden_movies(self.application)
		self.render("home.html", user=user, flicks=flicks, movies=golden_movies)



