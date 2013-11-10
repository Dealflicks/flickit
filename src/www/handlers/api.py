import tornado.web

import handlers.base

import utils.validationmixin

import tornado.escape

import models.flick
import models.movie

class JSONPHandler(handlers.base.BaseHandler):
    
    def write(self, callback, stuff):
        super(JSONPHandler, self).write(callback + '(' + tornado.escape.json_encode(stuff) + ')')
        self.set_header('Content-Type', 'application/javascript')

class FlickCountHandler(JSONPHandler):
    # def write(self, callback, stuff):
    #     super(FlickCountHandler, self).write(callback + '(' + tornado.escape.json_encode(stuff) + ')')
    #     self.set_header('Content-Type', 'application/javascript')

    def get(self):
        user = self.get_current_user()

        movie_id = self.valid("movie_id", int)
        ref = self.valid("ref", required=False)
        source = self.valid("source", required=False)
        callback = self.valid("callback", required=True)

        print movie_id
        print callback
       
        movie = models.movie.MovieModel.get_from_mysql_with_id(self.application, movie_id)

        flick = None
        has_flicked = False
        if user:
            flick = models.flick.FlickModel.get_from_mysql_with_movie_id_and_user_id(self.application, movie.id, user.id)

        if flick:
            has_flicked = True

        stuff = { 'movie_id' : movie.id, 'count' : movie.count, 'has_flicked' : has_flicked}

        self.write(callback, stuff)



class FlickCreateHandler(JSONPHandler):


    def get(self):
        # need to get user from cookie.
        user = self.get_current_user()

        # TODO: do something if user doesn't exist

        movie_id = self.valid("movie_id", int)
        callback = self.valid("callback", required=True)

        # TODO: do something if movie doesn't exist
        print movie_id
        movie = models.movie.MovieModel.get_from_mysql_with_id(self.application, movie_id)

        flick = models.flick.FlickModel.get_or_create(self.application, movie.id, user.id)

        has_flicked = False
        if flick:
            has_flicked = True

       
        stuff = { 'movie_id' : movie.id, 'count' : movie.count, 'has_flicked' : has_flicked}

        self.write(callback, stuff)



