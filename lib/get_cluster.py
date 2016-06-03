import pickle, re

def csv_to_list(f):
	pass

def get_cluster(filepath):
	""" Conventioin is that .csv files have all the meta-data and txt files have only the full tweets. """
	f = open(filepath, 'r')
	
	if(filepath.split('.')[-1] == 'csv'):
		csv_to_list(f)

	if(filepath.split('.')[-1] == 'txt'):
		cluster = ''
		for line in f.readlines():
			cluster += re.sub('\n',' ',line)

	return cluster