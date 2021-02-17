"""CONVERT SPOTIFY DATA TO TOPIC"""

def convert_to_topic(i):
	#take out non ascii characters
	i = i.encode('ascii',errors='ignore')
	i = i.decode()
    	#if invalid topic character in i replace with '-'
	invalid_chars = ["!","@","#",
					"$","%","^",
					"&","*","(",
					")","+","<",
					">",":","?",
					"/",".",",",
					"|","`","~"]
	for char in invalid_chars:
		if char in i:
			i = i.replace(char, '-')
    	#take out spaces and add to topic_name list
	return i.replace(" ", "")
