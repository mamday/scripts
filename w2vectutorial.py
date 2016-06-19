import pandas as pd
import nltk
from nltk import *
import sys

# Read data from files 
#train = pd.read_csv( "data/labeledTrainData.tsv", header=0, 
# delimiter="\t", quoting=3 )
#test = pd.read_csv( "data/testData.tsv", header=0, delimiter="\t", quoting=3 )
#unlabeled_train = pd.read_csv( "data/unlabeledTrainData.tsv", header=0, 
# delimiter="\t", quoting=3 )

in_str='HN'
text_str="comment_text"

in_data = pd.read_csv(sys.argv[1], header=0, delimiter=",", quotechar='"',skipinitialspace=True)

# Import various modules for string cleaning
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords

def review_to_wordlist( review, remove_stopwords=False ):
    # Function to convert a document to a sequence of words,
    # optionally removing stop words.  Returns a list of words.
    #
    #  
    review_text = review
    # 2. Remove non-letters
    review_text = re.sub("[^a-zA-Z]"," ", review_text)
    #
    # 3. Convert words to lower case and split them
    words = review_text.lower().split()
    #
    # 4. Optionally remove stop words (false by default)
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    #
    # 5. Return a list of words
    return(words)

# Load the punkt tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# Define a function to split a review into parsed sentences
def review_to_sentences( review, tokenizer, remove_stopwords=False ):
    # Function to split a review into parsed sentences. Returns a 
    # list of sentences, where each sentence is a list of words
    #
    #  Remove HTML
    review_text = BeautifulSoup(review,"lxml").get_text()
    # 1. Use the NLTK tokenizer to split the paragraph into sentences
    raw_sentences=[]
    try:
      raw_sentences = tokenizer.tokenize(review_text.strip())
    except:
      print 'Failed to parse',review_text.strip()
    #
    # 2. Loop over each sentence
    sentences = []
    for raw_sentence in raw_sentences:
        # If a sentence is empty, skip it
        if len(raw_sentence) > 0:
            # Otherwise, call review_to_wordlist to get a list of words
            sentences.append( review_to_wordlist( raw_sentence, \
              remove_stopwords ))
    #
    # Return the list of sentences (each sentence is a list of words,
    # so this returns a list of lists
    return sentences

sentences = []  # Initialize an empty list of sentences

#for review in in_data["comment_text"]:
for review in in_data[text_str]:
    sentences += review_to_sentences(review, tokenizer)

import gensim
from gensim import corpora, models, similarities
from gensim.models import word2vec

dictionary = corpora.Dictionary(sentences)
dictionary.save(in_str+'dict.dict')
corpus = [dictionary.doc2bow(sentence) for sentence in sentences]
corpora.MmCorpus.serialize(in_str+'corpus.mm', corpus)

# Import the built-in logging module and configure it so that Word2Vec 
# creates nice output messages
def Word2Vec(sentences):
  import logging
  logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',\
    level=logging.INFO)

# Set values for various parameters
  num_features = 300    # Word vector dimensionality                      
  min_word_count = 40   # Minimum word count                        
  num_workers = 4       # Number of threads to run in parallel
  context = 10          # Context window size                                                                                    
  downsampling = 1e-3   # Downsample setting for frequent words

# Initialize and train the model (this will take some time)
  from gensim.models import word2vec
  print "Training model..."
  model = word2vec.Word2Vec(sentences, workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)

# If you don't plan to train the model any further, calling 
# init_sims will make the model much more memory-efficient.
  model.init_sims(replace=True)

# It can be helpful to create a meaningful model name and 
# save the model for later use. You can load it later using Word2Vec.load()
  model_name = in_str+"_300features_40minwords_10context"
  model.save(model_name)

  #model.doesnt_match("france england germany berlin".split())

  #model.most_similar("man")
  #model.most_similar("queen")
  #model.most_similar("king")

Word2Vec(sentences)
