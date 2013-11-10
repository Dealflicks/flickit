import tornado.web

import handlers.base

import utils.validationmixin

import tornado.escape


class JSONPHandler(handlers.base.BaseHandler):
    
    def write(self, callback, stuff):
        super(JSONPHandler, self).write(callback + '(' + tornado.escape.json_encode(stuff) + ')')
        self.set_header('Content-Type', 'application/javascript')

class FlickCountHandler(JSONPHandler):
    # def write(self, callback, stuff):
    #     super(FlickCountHandler, self).write(callback + '(' + tornado.escape.json_encode(stuff) + ')')
    #     self.set_header('Content-Type', 'application/javascript')

    def get(self):

        movie_id = self.valid("movie_id", int)
        ref = self.valid("ref", required=False)
        source = self.valid("source", required=False)
        callback = self.valid("callback", required=True)

        print movie_id
        print callback
       
        stuff = { 'count' : 1 }

        self.write(callback, stuff)



class FlickCreateHandler(JSONPHandler):


    def get(self):
        # need to get user from cookie.
        user = self.get_current_user()

        print user

        movie_id = self.valid("movie_id", int)
        callback = self.valid("callback", required=True)

        print movie_id
       
        stuff = { 'count' : 2 }

        self.write(callback, stuff)



