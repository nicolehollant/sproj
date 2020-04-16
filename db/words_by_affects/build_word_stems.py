import json
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from scipy.sparse import csc
import pandas as pd
from pprint import pprint
import requests

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
    
# create sample documents
all_affects = json.load(open('words_by_affect.json', 'r'))

res = {}

def requestWord(word, collection='senselevel'):
  headers = {
    'Content-Type': 'application/json', 
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
  }
  url = 'http://localhost:5000/score'
  text = ' '.join(word)
  if not text: text = ''
  response = requests.post(url, data=json.dumps({ 'text': text, 'ignore': True }), headers=headers)
  return response.status_code, response.json()

def score_stem(stem, words):
  status, response = requestWord(words)
  if status == 200:
    res[stem]['score'] = response['data']
  else:
    res[stem]['score'] = { 'anger': 0.0, 'fear': 0.0, 'joy': 0.0, 'sadness': 0.0 }

# loop through document list
for emotion, words in all_affects.items():
  # remove stop words from words
  stopped_tokens = [i for i in words if not i in en_stop]
  # stem tokens and put in dict
  for word in stopped_tokens:
    stem = p_stemmer.stem(word)
    if stem in res and word not in res[stem]['words']:
      res[stem]['words'].append(word)
    else:
      res[stem] = { 'words': [word] }
  # add tokens to list

# pprint(res)
i = 0
for stem, data in res.items():
  i += 1
  if i % 10 == 0:
    print(i)
  # print(stem, data, data['words'])
  score_stem(stem, data['words'])

with open('stems-scores.json', 'w') as f:
  json.dump(res, f, sort_keys = True, indent = 2)