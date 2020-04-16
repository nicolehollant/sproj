import json
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from scipy.sparse import csc
import pandas as pd
from gensim.test.utils import datapath
from nltk.tokenize import RegexpTokenizer

'''
So, the idea is that we seed the model with 4 documents (one for each emotion that we care about)
Then, from there, we let it figure out its own topic mixture. This is a some linear combination of word_stems.
  i.e.: topic 96 is: (96, '0.002*"depress" + 0.002*"devast" + 0.002*"pain" + 0.002*"reject" + 0.001*"disapprov" + 0.001*"regret" + 0.001*"banish" + 0.001*"abandon" + 0.001*"poison" + 0.001*"murder"')
then we would want to grab a score from that.
- define scores for each topic
  - go through all words in topic get frequency of affects by topic
  - maybe targeting keywords in replacement?
    - maybe only score keywords?
- consider running through old model and multiplying by that scalar?
- also consider giving the inverting the topic keywords (restem?)
  - might actually be necessary to do this to get score!!!
  - think I'm going to have to add a whole bunch to both lexicons
    Kinda like this
    - wordstem: {
      words: [word1, word2, ...],
      affect_list: [...],
      sense_list: [...]
    },
    - wordstem: {
      words: [word1, word2, ...],
      angry: 123,
      sad: 134,
      joy: 48
    }
'''



def train():
  tokenizer = RegexpTokenizer(r'\w+')
  stopwords = ['ve', 'won', 'more', 'needn', "doesn't", 'most', 'each', 'down', 'should', "weren't", 'yourself', "didn't", 'on', 'below', 'whom', 'herself', 'your', "you'd", 'hers', 'you', 'about', 'because', 'up', 'me', 'can', 'out', "hasn't", 'him', 'again', 'is', 'same', 'were', 'a', "wasn't", 'd', "haven't", 'them', 'very', 'i', 'such', 'mightn', 'until', "mustn't", 'haven', 'off', 'here', 'it', 'isn', "won't", 'over', "that'll", 'the', "hadn't", 'wouldn', 'yourselves', 'was', 'we', 'both', 'doesn', 'been', 'when', "wouldn't", 'only', 'aren', 'has', 'why', 'do', 'weren', 'at', 't', 'from', 'how', 's', 'these', 'for', 'be', 'through', 'ourselves', 'to', 'where', 'of', "you're", 'in', 'he', "aren't", "shouldn't", "you'll", 'nor', 'didn', 'above', 'couldn', 'himself', 'than', 'hasn', 'they', 'so', 'm', 'but', 'other', "couldn't", 'll', 'its', 'then', 'there', 'some', 'too', 'shan', 'no', "she's", 'wasn', 're', 'hadn', 'being', 'what', 'this', 'are', 'our', 'myself', 'she', 'and', "isn't", 'does', 'that', 'while', 'own', 'having', 'against', 'had', 'by', 'their', 'my', 'did', 'shouldn', 'during', 'ma', 'now', 'or', 'into', 'few', 'themselves', 'once', "don't", 'her', 'any', 'will', 'ours', 'further', 'his', 'with', "shan't", "should've", 'just', 'after', "you've", 'yours', 'between', 'before', 'itself', 'theirs', 'ain', 'those', 'am', 'not', 'all', 'o', "mightn't", 'which', "it's", "needn't", 'who', 'under', 'y', 'mustn', 'if', 'have', 'an', 'doing', 'as', 'don']
  porter_stemmer = PorterStemmer()
  
  all_affects = json.load(open('lda/words_by_affect.json', 'r'))
  anger = " ".join(all_affects['anger'])
  fear = " ".join(all_affects['fear'])
  joy = " ".join(all_affects['joy'])
  sadness = " ".join(all_affects['sadness'])
  
  texts = [] # list for tokenized documents in loop
  for document in [anger, fear, joy, sadness]: # loop over docs
    tokens = tokenizer.tokenize(document.lower())
    stemmed_tokens = [porter_stemmer.stem(i) for i in tokens if not i in stopwords]
    texts.append(stemmed_tokens)

  # make dictionary to preserve words
  dictionary = corpora.Dictionary(texts)
  # give array of bag of words as corpus to our model. Use defaults for num_topics and passes
  ldamodel = gensim.models.ldamodel.LdaModel(
    [dictionary.doc2bow(text) for text in texts], 
    id2word=dictionary, 
    num_topics=100, 
    passes=20)
  ldamodel.save("lda/ldamodel")