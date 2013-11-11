import string
import random
import pycurl
from cStringIO import StringIO
#import pprint
from lxml.html import fromstring
import nltk
import urllib
import urllib2
import base64
import json
from PIL import Image
from boto.s3.connection import S3Connection
from boto.s3.key import Key

import tornado.escape

def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))


def get_best_for_image(img_url):
	url = "https://www.google.com/searchbyimage?&image_url=%s" % tornado.escape.url_escape(img_url)

	b = StringIO()
	c = pycurl.Curl()
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.REFERER, 'http://www.helloworld.com')
	c.setopt(pycurl.SSL_VERIFYPEER, False)
	c.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11')
	c.setopt(pycurl.FOLLOWLOCATION, True)
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	c.perform()
	c.close()

	doc = fromstring(b.getvalue())
	el = doc.find_class('qb-bmqc')
	if len(el) == 0:
		return False

	img_texts = el[0].text_content().split(':')

	return img_texts[1].strip()


def get_movie_for_best_guess(movies, img_text):
	# request = urllib2.Request("https://api.dealflicks.com/movies/")
	# base64string = base64.encodestring('%s:%s' % ("dealflick$_$ecret_key", "")).replace('\n', '')
	# #print base64string
	# #request.add_header("Authorization", "Basic %s" % base64string)   
	# request.add_header("Authorization", "Basic ZGVhbGZsaWNrJF8kZWNyZXRfYXBpOg==")   
	# response = urllib2.urlopen(request)

	# movies = json.loads(response.read())
	#movies = db.query("SELECT id, name FROM movie ORDER BY name ASC")
	k = -1
	best_id = 0
	best_movie = ""
	for movie in movies:
		l = nltk.metrics.distance.edit_distance(img_text.lower(), movie.name.lower())
		if(l<k or k == -1):
			k=l
			best_id=movie.id
			best_movie=movie.name

	our_movie = { 'id': best_id, 'movie': best_movie, 'nltk': k}
	return our_movie


def access_s3():
	aws_key = "AKIAJCQQIW75QZX6LPGA"
	aws_secret = "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"
	conn = S3Connection(aws_key, aws_secret)
	b = conn.get_bucket('flickit-static')
	k = Key(b)
	return k


def edit_and_upload_image(image, key_name=None):
	imgbuf = edit_image(image)
	return upload_image(imgbuf, key_name)

def edit_image(image):
	im = Image.open(StringIO(urllib.urlopen(image).read()))
	img_size = im.getbbox()
	new_y = (img_size[3] * 2) / 3
	new_x = new_y * (0.675)
	start_y = (img_size[3] - new_y) / 2
	start_x = (img_size[2] - new_x) / 2

	new_size = int(start_x), int(start_y), int(start_x + new_x), int(start_y + new_y)
	new_im = im.crop(new_size)
	imgbuf = StringIO()
	new_im.save(imgbuf, "JPEG")
	return imgbuf

def upload_image(imgbuf, key_name=None):
	k = access_s3()

	if key_name is None:
		key_name = id_generator()

	k.key = "images/%s.jpg" % key_name
	k.set_contents_from_string(imgbuf.getvalue())
	k.make_public()
	return (key_name, k.generate_url(120).split('?')[0])


def get_attr_or_default(unidentified_object, attr_name, default_value=None):
    if type(unidentified_object) == dict:
        return unidentified_object.get(attr_name, default_value)
    else:
        try:
            return getattr(unidentified_object, attr_name, default_value)
        except Exception, e:
            return default_value