#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import couchdb
import sys
import time

#Variables that contains the user credentials to access Twitter API 
access_token = "540579376-1f65ZblgI5wIBb3fH6IU4XJ5jVkvqtnyPkMRE9Ad"
access_token_secret = "e2UVGhw5vrYdD7ShQFQ49yG2QbxdtfqYIAVyhaIv8INtL"
consumer_key = "t6MwuVuO0tL6POvNtY8wDVuyY"
consumer_secret = "fpGOkk1BmJVUPhKSOBtbnv69RnSySH0axozOiWHN4x231ozNAi"

couch = couchdb.Server('http://115.146.89.147:5984/')
dbname = 'comp90024'
try:
    db = couch[dbname]
    print "opened",dbname
except couchdb.ResourceNotFound:
    print "creating db",dbname
    db = couch.create(dbname)

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_connect(self):
        print("You're connected to the streaming server.")

    # def on_data(self, data):
    #     print data
    #     #cid, rev = db.save(data)
    #     #print cid
    #     return True

    def on_status(self, status):
        global db # couchdb (global)
        try:
            print status.created_at
            # skip retweets
            if status.retweet_count:
                return True
            # skip if already in couch
            if status.id_str in db:
                return True
            results = {}
            # status info. See: https://dev.twitter.com/docs/api/1/get/statuses/show/%3Aid
            results['text']=status.text.lower()
            results['orig_text']=status.text
            results['id_str']=status.id_str
            results['created_at'] = time.asctime(time.localtime(time.mktime(status.created_at.utctimetuple())))
            #time.mktime(status.created_at.utctimetuple())
            results['entities'] = status.entities # urls, hashtags, mentions,
            results['source'] = status.source
            results['geo'] = status.geo
            # results['location'] = status.location
            results['lang'] = status.lang
            results['retweet_count'] = status.retweet_count
            results['retweeted'] = status.retweeted
            db.save(results)
            print results
        except Exception, e:
            print sys.stderr, 'Encountered Exception:', e#.get_trace()
            pass

        return True

    def on_error(self, status):
        print status
        if status == 420:
            #returning False in on_data disconnects the stream
            return False


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(track=['python', 'javascript', 'ruby'])
    # get geo box http://boundingbox.klokantech.com/  -csv raw
    stream.filter(locations=[-180,-90,180,90])
    #stream.filter(locations=[105.3756965399,-44.6530241598,164.35546875,-10.1851874093])
