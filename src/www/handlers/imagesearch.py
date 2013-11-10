import utils.utils
import handlers.base
from cStringIO import StringIO
import tornado.escape

import models.flick
import models.movie

class PictureHandler(handlers.base.BaseHandler):

    def cycle_the_filter(self, img_url, key_name, edit_count):
    	img_text = False
    	while img_text == False:
        	key_name, img_url = utils.utils.edit_and_upload_image(img_url, key_name)
        	edit_count += 1
        	img_text = utils.utils.get_best_for_image(img_url)
        	if edit_count == 3:
        		break

        return (img_text, img_url, key_name, edit_count)

    def search_for_image(self, org_img_url, key_name=None):
    	if (self.errors):
            return self.send_error(400, chunk={'Status' : 'Error', 'Errors' : self.errors })

        img_url = org_img_url
        img_text, img_url, key_name, edit_count = self.cycle_the_filter(img_url, key_name, 0)   

        if img_text == False:
        	return self.send_error(400, chunk={'Status' : 'Error', 'Errors' : self.errors })

        movies = self.mysqldb.query("SELECT id, name FROM movie ORDER BY name ASC")

        our_movie = utils.utils.get_movie_for_best_guess(movies, img_text)
        movie_id = our_movie['id']
        movie_name = our_movie['movie']
        movie_nltk = our_movie['nltk']
    	if movie_nltk > 18 and edit_count < 3:
    		key_name, img_url = utils.utils.edit_and_upload_image(img_url, key_name)
        	img_text = utils.utils.get_best_for_image(img_url)
        	if img_text != False:
        		our_movie = utils.utils.get_movie_for_best_guess(movies, img_text)

        if our_movie['nltk'] < movie_nltk:
        	movie_id = our_movie['id']
        	movie_name = our_movie['movie']
        	movie_nltk = our_movie['nltk']

        return (movie_id, movie_name, movie_nltk)

class PictureSearchHandler(PictureHandler):

    def post(self):
    	org_img_url = self.valid('imgurl', str, required=True)
    	id, name, nltk = self.search_for_image(org_img_url)
    	self.write("movie_id: %s" % id)


class PictureSearchByStringHandler(PictureHandler):

    def post(self):
    	img_string = self.valid('imgstr', str, required=True)
    	imgbuf = StringIO()
    	imgbuf.write(img_string)
    	org_img_url, key_name = utils.utils.upload_image(imgbuf)
    	id, name, nltk = self.search_for_image(org_img_url, key_name)
    	self.write("movie_id: %s" % id)   

class JSONPHandler(PictureHandler):
    
    def write(self, callback, stuff):
        super(JSONPHandler, self).write(callback + '(' + tornado.escape.json_encode(stuff) + ')')
        self.set_header('Content-Type', 'application/javascript')

class ImageSearchHandler(JSONPHandler):

    def get(self):
    	org_img_url = self.valid('imgurl', str, required=True)
        callback = self.valid("callback", required=True)

    	movie_id, name, nltk = self.search_for_image(org_img_url)

        user = self.get_current_user()

        movie = models.movie.MovieModel.get_from_mysql_with_id(self.application, movie_id)
        flick = models.flick.FlickModel.get_or_create(self.application, movie.id, user.id)

        has_flicked = False
        if flick:
            has_flicked = True

       
        stuff = { 'movie_id' : movie.id, 'count' : movie.count, 'has_flicked' : has_flicked}

        self.write(callback, stuff)

