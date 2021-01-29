from creds import *
hst = c_host
usr = c_user
pw = c_pw
nme = c_name

import mysql.connector
import csv
from datetime import date


#queries
selectq="SELECT * FROM data"
dropq="DROP TABLE IF EXISTS data"

#store date for csv file name
today = date.today()


def db_dump_reset():
	db = mysql.connector.connect(
		host=hst,
		port=3306,
		user=usr,
		passwd=pw,
		database=nme 
		)
	mycursor = db.cursor()

	#select fields and store CSV, only reset table on success
	try:
		#select fields and store in data
		mycursor.execute(selectq)
		data = mycursor.fetchall()

		#write to csv
		with open(f'./db_archives/{today.strftime("%b-%d-%Y")}.csv', 'w', newline='') as csv_file:
			csv_writer = csv.writer(csv_file)
			csv_writer.writerow([i[0] for i in mycursor.description]) #write headers
			csv_writer.writerows(data) #write rows

	except Exception as e:
		print(f'Unsuccessful creating CSV snapshot: {e}')

	#if CSV created reset tables
	else:
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
		db.commit()


#run script
db_dump_reset()
	
