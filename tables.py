"""CREATE TABLES"""

from creds import *
hst = c_host
usr = c_user
pw = c_pw
nme = c_name

import mysql.connector

#connect to db
def create_tables():
	db = mysql.connector.connect(
		host=hst,
		port=3306,
		user=usr,
		passwd=pw,
		database=nme 
		)
	mycursor = db.cursor()

	#drop table
	mycursor.execute("""DROP TABLE IF EXISTS data""")

	#create table
	mycursor.execute("""
		CREATE TABLE data
			(topic VARCHAR(100),
			tweet VARCHAR(250),
			date_added DATETIME
			)
			""")
	#commit changes
	db.commit()


#run script
create_tables()

