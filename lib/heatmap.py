import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def heatmap(file_in = '../corpora/coords.csv' ,file_out='../img/highres_heatmap.png', resolution = 600):
	x, y = [], []
	# waarin elke regel in coords.csv als volgt is:
	# '5.6274467\t51.5283918\n'
	with open(file_in) as f:
	    for line in f.readlines():
	        line = line.rstrip().split("\t")
	        line = line[0].split(" ")
	        x.append(float(line[0]))
	        y.append(float(line[1]))

	plt.hist2d(x, y, (resolution, resolution), norm=LogNorm())
	plt.colorbar()
	plt.savefig(file_out)
	plt.close()