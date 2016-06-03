from lib.get_cluster import *
from lib.clean_texts import *
from lib.tfidf import *
from lib.clusters import *
from lib.pushover import *
import pickle

def dorpen():
	f = open('pickles/dorpen.pickle','rb')
	dorpen = pickle.load(f)
	# left out 'groningen, groningen', same name for province and city are too easily processed wrongly
	titles = ['aalten','almelo','amersfoort','assen','delft','emmen','groesbeek','haarlem','hattem','heerhugowaard','helmond','kerkrade','leeuwarden','lochem','middelburg','nunspeet','oldebroek','ommen','oosterhout','putten','roosendaal','schagen','schiermonnikoog','soest','staphorst','urk','veendam','venlo','venray','vianen']
	villages = []
	for title in titles:
		villages.append(" ".join(dorpen[title]))
	clusters = [titles, villages]

	# second, clean the clusters from e.g. url's and punctuation
	pushover(message='Starting clean_texts')
	clean_texts(clusters, pushover=False,username=True,punctuation=True,url=True,stopword=True,numbers=True)
	pushover(message='Done with clean_texts')

	pushover(message='Creating tf-idf')
	# thrid, create tf-idf matrix and save matrix out to file
	tfidf_matrix, dist = create_tfidf(clusters, filename='pickles/dorpen_punc_sw_url_usr.pickle')

	# fourth, create hierarchical cluster (ward algorithm)
	ward_cluster(clusters[0],dist,filename='img/dorpen_punc_sw_url_usr.png')
	pushover(message='Ward created')

def provincies():
	# first, create the clusters
	titles = ['drenthe','flevoland','friesland','gelderland','groningen','limburg','noord_brabant','noord_holland','overijssel','utrecht','zeeland','zuid_holland']
	clusters = [titles,[]]
	for title in titles:
		filename = '../../corpora/provincies/' + title + '.txt'
		clusters[1].append(get_cluster(filename))

	# second, clean the clusters from e.g. url's and punctuation
	pushover(message='Starting clean_texts')
	clean_texts(clusters, username=True,punctuation=True,url=True,stopword=True,numbers=True)
	pushover(message='Done with clean_texts')

	pushover(message='Creating tf-idf')
	# thrid, create tf-idf matrix and save matrix out to file
	tfidf_matrix, dist = create_tfidf(clusters, filename='pickles/provinces_punc_sw_url_usr.pickle')

	# fourth, create hierarchical cluster (ward algorithm)
	ward_cluster(clusters[0],dist,filename='img/provinces_punc_sw_url_usr.png')
	pushover(message='Ward created')

def main():
	#provincies()
	dorpen()

if __name__ == '__main__':
	main()