"""KAFKA CONSUMER"""

from creds import *
hst = c_host
usr = c_user
pw = c_pw
nme = c_name

from kafka import KafkaConsumer
import json
import time
import mysql.connector
import time
from spotify import *
from global_functions import *


#get Spotify data from get_playlist_data imported from Spotify module
sl = get_playlist_data('spotify:playlist:37i9dQZF1DX4JAvHpjipBk')

#strip non kafka-compatable characters (pass strings to topic_name list)
topic_name = []
for i in sl:
	topic_name.append(convert_to_topic(i))

#kafka consumer parameters
consumer = KafkaConsumer(
	*topic_name,
	bootstrap_servers=['localhost:9092'],
	auto_offset_reset='latest',
	enable_auto_commit=True,
	auto_commit_interval_ms =  5000,
	fetch_max_bytes = 128,
	max_poll_records = 100,
	value_deserializer=lambda x: json.loads(x.decode('utf-8')))


def post_data():
	db = mysql.connector.connect(
		host=hst,
		port=3306,
		user=usr,
		passwd=pw,
		database=nme 
		)
	mycursor = db.cursor()

	#POST data
	for message in consumer:
		dt = time.strftime('%Y-%m-%d %H:%M:%S')
		tweets = json.loads(json.dumps(message.value))
		for key, value in tweets.items():
			if key == 'text':

				mycursor.execute("""
					INSERT INTO data
						(topic,
						tweet,
						date_added
						)
					VALUES (%s,%s,%s)
					""",
						(	message.topic,
							value,
							dt
						))

				#post to terminal
				print(f"TOPIC: {message.topic}")
				print(f"TWEET: {value}")
				print(f"DATETIME: {dt}")
 				
		#commit changes
		db.commit()


post_data()










	
