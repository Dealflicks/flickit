import tornado.web

import handlers.base

import models.movie

class WidgetBuilderHandler(handlers.base.BaseHandler):

    def get(self):
        preselected_movie_id = self.valid("movie_id", int, required=False)
        print preselected_movie_id

        movies = models.movie.MovieModel.get_all_movies_from_mysql_ordered_alphabetically(self.application)
   
        self.render("widget_builder.html", movies=movies, preselected_movie_id=preselected_movie_id)
