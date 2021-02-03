
from creds import *
consumer_key = c_consumer_key
consumer_secret = c_consumer_secret
access_token = c_access_token
access_token_secret = c_access_token_secret


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
from spotify import *
from global_functions import *


#get Spotify data from get_playlist_data imported from Spotify module
sl = get_playlist_data('spotify:playlist:37i9dQZF1DX4JAvHpjipBk')

#strip non kafka-compatable characters (pass strings to topic_name list)
topic_name = []
for i in sl:
    topic_name.append(convert_to_topic(i))

#kafka producer parameters
producer = KafkaProducer(bootstrap_servers='localhost:9092')



#twitter AUTH
class twitterAuth():
    """SET UP TWITTER AUTHENTICATION"""

    def authenticateTwitterApp(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth



#kafka listener
class ListenerTS(StreamListener):

    def on_data(self, raw_data):
        for s in sl:
            if s.encode(encoding='UTF-8') in str.encode(raw_data):
                producer.send(convert_to_topic(s), str.encode(raw_data))
        print(raw_data)
        return True
    def on_error(self, status):
        print(status)



#twitter streamer
class TwitterStreamer():

    #set up streamer
    def __init__(self):
        self.twitterAuth = twitterAuth()

    def stream_tweets(self):
        while True:
            listener = ListenerTS() 
            auth = self.twitterAuth.authenticateTwitterApp()
            stream = Stream(auth, listener)
            stream.filter(track=sl, stall_warnings=True, languages= ["en"])



#run program
if __name__ == "__main__":
    TS = TwitterStreamer()
    TS.stream_tweets()

    




