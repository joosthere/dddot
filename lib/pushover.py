import http.client, urllib

def pushover(message = 'Done running script.', title = 'Clustering'):
	""" Sends a push notification to the Pushover Android application.
	In this case, the phone of @Joosthere. """
	try:
		conn = http.client.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
			urllib.parse.urlencode({
		    	"token": "ayo3GoW5ccWYUZSbQyw3PaY8yjxzpJ",
		    	"user": "uYj2hJb4EHLrgMtx1Ar8EnCtwukR2B",
		    	"message": message,
		    	"title": title
		  	}), 
		  	{ "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()
	except:
		pass