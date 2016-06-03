""" Partly from http://brandonrose.org/clustering """
import uuid
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import ward, dendrogram
from sklearn.metrics.pairwise import cosine_similarity

def ward_cluster(titles, dist, filename = ''):
	""" Creates a .png file, containing a hierarchical clustering of the cosine cluster vectors in $dist.
	If $filename is not passed as parameter a uuid.uuid4() will be used as filename. """
	try:
		linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances
	except:
		dist = 1 - cosine_similarity(dist)
		linkage_matrix = ward(dist)
	
	fig, ax = plt.subplots(figsize=(6, 8)) # set size
	ax = dendrogram(linkage_matrix, orientation="left", labels=titles)

	plt.tick_params(\
	    axis= 'x',          # changes apply to the x-axis
	    which='both',      # both major and minor ticks are affected
	    bottom='off',      # ticks along the bottom edge are off
	    top='off',         # ticks along the top edge are off
	    labelbottom='off')

	plt.tight_layout() #show plot with tight layout
	if(filename == ''):
		filename = '../img/ward_clusters_' + str(uuid.uuid4()) + '.png'

	plt.savefig(filename, dpi=200) #save figure as ward_clusters
	plt.close()