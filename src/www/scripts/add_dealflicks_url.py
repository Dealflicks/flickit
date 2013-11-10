#!/usr/bin/python

import urllib2
import pprint
import json
import torndb
import base64

pp = pprint.PrettyPrinter(indent=4)

#rotten tomatoes api key: bz3epgfnmp5upw4prjd4y6rv

DEALFLICKS_DB_HOST		= "flickit.cithkcxnky7r.us-east-1.rds.amazonaws.com"
DEALFLICKS_DB_PORT 		= "3306"
DEALFLICKS_DB_NAME		= "flickit"
DEALFLICKS_DB_USER		= "flickit"
DEALFLICKS_DB_PASSWORD	= "launch2013"

db = torndb.Connection(
	host=DEALFLICKS_DB_HOST + ":" + DEALFLICKS_DB_PORT, database=DEALFLICKS_DB_NAME,
	user=DEALFLICKS_DB_USER, password=DEALFLICKS_DB_PASSWORD)

def movie_information(movie_id):
	request = urllib2.Request("https://api.dealflicks.com/movies/%s" % movie_id)
	#base64string = base64.encodestring('%s:%s' % ("dealflick$_$ecret_key", "")).replace('\n', '')
	#print base64string
	#request.add_header("Authorization", "Basic %s" % base64string)   
	request.add_header("Authorization", "Basic ZGVhbGZsaWNrJF8kZWNyZXRfYXBpOg==")   
	response = urllib2.urlopen(request)

	movie = json.loads(response.read())
	return movie


if __name__ == '__main__':
	print "Starting to update database"

	movies = db.query("SELECT id, dealflicks_movie_id from movie")
	for movie in movies:
		minfo = movie_information(movie['dealflicks_movie_id'])
		df_url = minfo['Dealflicks_URL']
		db.execute("UPDATE movie SET dealflicks_url=%s WHERE id = %s", df_url, movie['id'])

	print "Finished updating database"


