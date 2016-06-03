from lib.get_cluster import *
from lib.clean_texts import *
from lib.tfidf import *
from lib.clusters import *
from lib.pushover import *
import pickle
from sklearn.metrics.pairwise import cosine_similarity

def main():
	pickle_object = open('pickles/provinces.pickle','rb')
	tfidf_matrix = pickle.load(pickle_object)
	dist = 1 - cosine_similarity(tfidf_matrix) 
	ward_cluster(['drenthe','flevoland','friesland','gelderland','groningen','limburg','noord_brabant','noord_holland','overijssel','utrecht','zeeland','zuid_holland'],dist,filename='img/provinces.png')
	pushover(message='Ward created')

if __name__ == '__main__':
	main()