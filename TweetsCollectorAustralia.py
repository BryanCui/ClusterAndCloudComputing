import couchdb
import httplib
import tweepy
import json

ACCESS_TOKEN = '726231819289382912-z7VrMFkGq1xJTTBiVSFtNOP1H0ctDOW'
ACCESS_SECRET = 'nU4iLfPzcmxsVaZ7ZE0YEJKndoDCGW6JyV9FnWOicRD7a'
CONSUMER_KEY = '1rx2B1kw9FeZIGjVtkf01u3rG'
CONSUMER_SECRET = 'W3s4Mxj8TuXBgWcJkiZSPoXkR6ItE60WdL9XqwRXt8zkQ9sI4t'

class StreamListener(tweepy.StreamListener):
	def on_data(self, data):
		try:
			#print data
			database = connect_couch_database()
			save_data_into_database(database, json.loads(data))
		except BaseException, e:
			print 'What happened: ', str(e)
	def on_status(self, status):
		print(status)
		
	def on_error(self, status):
		print status

def connect_couch_database():
	couch_database = couchdb.Server('http://127.0.0.1:5984/')
	cloud_tweets = couch_database['cloud_tweets_australia']
	return cloud_tweets

def save_data_into_database(database, tweet):
	database.save(tweet)

def stream_twitter():	
	
	oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	oauth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	api = tweepy.API(oauth)
	stream_listener = StreamListener()
	tweet_stream = tweepy.streaming.Stream(auth=api.auth, listener=stream_listener)
	tweet_stream.filter(locations=[96.8168,-43.7405,159.1092,-9.1422])


stream_twitter()	
