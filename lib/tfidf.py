""" Partly from http://brandonrose.org/clustering """
import timeit, nltk, pickle, uuid
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import feature_extraction
import matplotlib.pyplot as plt
try:
	from pushover import *
except:
	from lib.pushover import *

def tokenize_only(text):
    """Uses the nltk.sent_tokenize() and nltk.word_tokenize()."""
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    return tokens

def tokenize_and_stem(text):
    """Uses the nltk.sent_tokenize() and nltk.word_tokenize().
    Furthermore, it uses the nltk.stem.snowball.SnowbalStemmer for the Dutch language."""
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    stemmer = SnowballStemmer('dutch')
    stems = [stemmer.stem(t) for t in tokens]
    return stems

def get_n_features(titles, tfidf_vectorizer, tfidf_matrix, n=25):
    """ Get the n-most representative features for each document. 
    Also writes out the entine list per document out to file."""

    features = tfidf_vectorizer.get_feature_names()
    top_lists = [titles, []]

    for doc in tfidf_matrix:
        zipped = zip(doc.data, doc.indices)
        sortedwords = [features[ind] for data, ind in reversed(sorted(zipped))]
        top_lists[1].append(sortedwords)
        print(titles.pop().capitalize())
        print(sortedwords[:n])
        print()
    
    with open('top_words_lists.pickle', 'wb') as f:
        pickle.dump(top_lists, f)

def create_tfidf(texts, filename = '', top_n = 25):
    """Creates tf-idf matrix from the selected clusters.
    Uses the sklearn.feature_extraction.text.TfidfVectorizer to do so.
    $filename is to write out the sparse matrix to a pickle file ater completion.
    If filename is not passed as parameter, a uuid.uuid4() will be used as filename."""

    tic=timeit.default_timer()

    # creating the tf-idf matrix
    tfidf_vectorizer = TfidfVectorizer(max_df=0.9, min_df=0.2, use_idf=True, tokenizer=tokenize_only) # or tokenize_and_stem, max used to be 0.8
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts[1])
    dist = 1 - cosine_similarity(tfidf_matrix)

    toc=timeit.default_timer()

    message = str(int(toc-tic)) + ' seconds to complete matrix. Shape: ' + str(tfidf_matrix.shape)
    pushover(message=message)

    get_n_features(texts[0][::-1], tfidf_vectorizer, tfidf_matrix, top_n)

    # saving the tf-idf matrix
    if(filename == ''):
    	filename = '../pickles/' + str(uuid.uuid4()) + '.pickle'

    with open(filename, 'wb') as f:
    	pickle.dump(tfidf_matrix, f)

    return tfidf_matrix, dist