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


def list_of_movies():
	request = urllib2.Request("https://api.dealflicks.com/movies/")
	#base64string = base64.encodestring('%s:%s' % ("dealflick$_$ecret_key", "")).replace('\n', '')
	#print base64string
	#request.add_header("Authorization", "Basic %s" % base64string)   
	request.add_header("Authorization", "Basic ZGVhbGZsaWNrJF8kZWNyZXRfYXBpOg==")   
	response = urllib2.urlopen(request)

	movies = json.loads(response.read())
	return movies


def movie_information(movie_id):
	request = urllib2.Request("https://api.dealflicks.com/movies/%s" % movie_id)
	#base64string = base64.encodestring('%s:%s' % ("dealflick$_$ecret_key", "")).replace('\n', '')
	#print base64string
	#request.add_header("Authorization", "Basic %s" % base64string)   
	request.add_header("Authorization", "Basic ZGVhbGZsaWNrJF8kZWNyZXRfYXBpOg==")   
	response = urllib2.urlopen(request)

	movie = json.loads(response.read())
	return movie


def get_rotten_tomatoes(rt_id):
	rt_api = "bz3epgfnmp5upw4prjd4y6rv"
	url = "http://api.rottentomatoes.com/api/public/v1.0/movies/%s.json?apikey=%s" % (rt_id, rt_api)
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	
	movie_info = json.loads(response.read())
	return movie_info


def update_database(movie):
	db.execute("""INSERT INTO movie (dealflicks_movie_id, name, poster, critics_score, audience_score, duration, mpaa_rating, 
		genre, abridged_cast, synopsis, theater_release_date, rotten_tomatoes_id)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
		""", movie['dealflicks_movie_id'], movie['name'], movie['poster'], movie['critics_score'], movie['audience_score'], movie['duration'], 
		movie['mpaa_rating'], movie['genre'], movie['abridged_cast'], movie['synopsis'], movie['theater_release_date'], movie['rotten_tomatoes_id'])


if __name__ == '__main__':
	print "Starting to update database"

	movies = list_of_movies()
	for movie_id, movie_name in movies.iteritems():
		movie_info = {}
		movie = movie_information(movie_id)
		if movie['Id'] == 0:
			continue

		movie_info['dealflicks_movie_id'] = movie['Id']
		movie_info['name'] = movie['Name']
		movie_info['duration'] = movie['Duration']
		movie_info['mpaa_rating'] = movie['Mpaa_rating']
		movie_info['rotten_tomatoes_id'] = movie['Rotten_tomatoes_id']
		movie_info['poster'] = None
		movie_info['critics_score'] = None
		movie_info['audience_score'] = None
		movie_info['genre'] = None
		movie_info['abridged_cast'] = None
		movie_info['synopsis'] = None
		movie_info['theater_release_date'] =  None

		if movie['Rotten_tomatoes_id'] is not None and movie['Rotten_tomatoes_id'] != "":
			movie_rt = get_rotten_tomatoes(movie['Rotten_tomatoes_id'])
			movie_info['poster'] = movie_rt['posters']['original']
			movie_info['critics_score'] = movie_rt['ratings']['critics_score']
			movie_info['audience_score'] = movie_rt['ratings']['audience_score']
			movie_info['genre'] = ', '.join(movie_rt['genres'])
			movie_info['abridged_cast'] = ', '.join([ actor['name'] for actor in movie_rt['abridged_cast'] ])
			movie_info['synopsis'] = movie_rt['synopsis']
			movie_info['theater_release_date'] = movie_rt['release_dates']['theater'] if 'theater' in movie_rt['release_dates'] else None

		#pp.pprint(movie_info)
		update_database(movie_info)

	print "Finished updating database"


