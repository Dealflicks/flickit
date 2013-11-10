import tornado.web

import handlers.base
import models.movie

class HomeHandler(handlers.base.BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()

        flicks = []
        if user:
          flicks = user.flicks

        golden_movies = models.movie.MovieModel.get_golden_movies(self.application)

        flick_ids = set()
        for flick in flicks:
            flick_ids.add(flick.movie_id)

        print flick_ids

        final_movies = []
        for movie in golden_movies:
            if movie.id not in flick_ids:
                final_movies.append(movie)

        self.render("home.html", user=user, flicks=flicks, movies=final_movies)



