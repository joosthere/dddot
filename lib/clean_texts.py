import re, nltk, string, timeit
from emoji import UNICODE_EMOJI
try:
	from pushover import pushover as psh
except:
	from lib.pushover import pushover as psh

def clean_texts(texts, pushover=True, stopword = False, username=False, punctuation = False, url = False, emoji = False, numbers = False):
	""" Where $texts is 2d list with texts[0][n] are titles for the texts[1][n] texts.
	Each parameter filters out that type for each text in texts[1].
	Stopwords uses the nltk.corpus.stopwords.words('dutch') corpus,
	the emoji uses the emoji.UNICODE_EMOJI set of emojis
	and the punctuation uses string.punctuation set of characters. 
	Also filters out Twitter usernames, urls and numbers by means of regular expressions."""

	emoji_list = list(UNICODE_EMOJI)

	stopwords = nltk.corpus.stopwords.words('dutch')

	tic=timeit.default_timer()

	for i in range(len(texts[0])):
		if(pushover):
			psh(message='At the ' + str(i+1) + 'th text to clean.')
		# remove dutch stopwords
		if(stopword):
			temp = texts[1][i].split(' ')
			texts[1][i] = ''
			words = []
			for word in temp:
				if word.lower() not in stopwords:
					words.append(word)
			texts[1][i] = " ".join(words)
			del(temp, words)

		if(username):
			temp = texts[1][i].split(' ')
			texts[1][i] = ''
			words = []
			for word in temp:
				if not word.startswith("@"):
					words.append(word)
			texts[1][i] = " ".join(words)
			del(temp, words)
			
		#if(hashtag):
			# empty for now, since punctuation removes the hashtag sign
		#	pass

		# remove punctuation
		if(punctuation):
			texts[1][i] = re.sub('['+string.punctuation+'°]','',texts[1][i]) # or - '°'
			
		# remove http's and https's
		if(url):
			texts[1][i] = re.sub(r'http\S+','',texts[1][i])

		if(numbers):
			temp = texts[1][i].split(' ')
			texts[1][i] = ''
			words = []
			for word in temp:
				try:
					x = int(word)
				except:
					words.append(word)
			texts[1][i] = " ".join(words)
			del(temp, words)
			
		# remove emojis
		if(emoji):
			for emoji in emoji_list:
				if emoji in texts[1][i]:
					texts[1][i].replace(emoji, '')
			
		# remove all newlines
		texts[1][i] = re.sub('\n','',texts[1][i])

		# remove multiple spaces
		texts[1][i] = re.sub(' +',' ',texts[1][i])

	toc=timeit.default_timer()
	duration = str(int(toc-tic))
	print(duration + ' seconds for cleaning texts.')

	return texts