import json
import os
from pprint import pprint
import sys
import requests
import numpy as np

affect_intensity = './NRC-Affect-Intensity-Lexicon/out/affect_intensity.json'
senselevel = './NRC-Emotion-Lexicon/senselevel/out/senselevel.json'
stopwords = ['ve', 'won', 'more', 'needn', "doesn't", 'most', 'each', 'down', 'should', "weren't", 'yourself', "didn't", 'on', 'below', 'whom', 'herself', 'your', "you'd", 'hers', 'you', 'about', 'because', 'up', 'me', 'can', 'out', "hasn't", 'him', 'again', 'is', 'same', 'were', 'a', "wasn't", 'd', "haven't", 'them', 'very', 'i', 'such', 'mightn', 'until', "mustn't", 'haven', 'off', 'here', 'it', 'isn', "won't", 'over', "that'll", 'the', "hadn't", 'wouldn', 'yourselves', 'was', 'we', 'both', 'doesn', 'been', 'when', "wouldn't", 'only', 'aren', 'has', 'why', 'do', 'weren', 'at', 't', 'from', 'how', 's', 'these', 'for', 'be', 'through', 'ourselves', 'to', 'where', 'of', "you're", 'in', 'he', "aren't", "shouldn't", "you'll", 'nor', 'didn', 'above', 'couldn', 'himself', 'than', 'hasn', 'they', 'so', 'm', 'but', 'other', "couldn't", 'll', 'its', 'then', 'there', 'some', 'too', 'shan', 'no', "she's", 'wasn', 're', 'hadn', 'being', 'what', 'this', 'are', 'our', 'myself', 'she', 'and', "isn't", 'does', 'that', 'while', 'own', 'having', 'against', 'had', 'by', 'their', 'my', 'did', 'shouldn', 'during', 'ma', 'now', 'or', 'into', 'few', 'themselves', 'once', "don't", 'her', 'any', 'will', 'ours', 'further', 'his', 'with', "shan't", "should've", 'just', 'after', "you've", 'yours', 'between', 'before', 'itself', 'theirs', 'ain', 'those', 'am', 'not', 'all', 'o', "mightn't", 'which', "it's", "needn't", 'who', 'under', 'y', 'mustn', 'if', 'have', 'an', 'doing', 'as', 'don']

def check_keys():
  with open(affect_intensity, 'r') as f:
    affect_intensity_data = json.load(f)
  # with open(senselevel, 'r') as f:
  #   senselevel_data = json.load(f)
    
  # affect_keys = affect_intensity_data.keys()
  # for key in senselevel_data.keys():
  #   if key not in affect_keys:
  #     print(key)
  affects = set()
  affect_vals = affect_intensity_data.values()
  for val in affect_vals:
    for dim in val:
      affects.add(dim.get('affect_dimension', None))
  affects = list(affects)
  for affect in affects:
    print(affect) # sadness joy fear anger



def requestWord(word, collection='senselevel'):
  headers = {
    'Content-Type': 'application/json', 
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
  }
  baseurl = 'https://sproj.api.colehollant.com/thesaurus/api/v1/' + collection + '/'
  url = baseurl + word
  response = requests.get(url, headers=headers)
  return response.status_code, response.json()

def get_synonyms(word):
  res = []
  code, thesaurus_response = requestWord(word, collection='words')
  if code == 200:
    synonyms_dict = thesaurus_response['data']['synonyms']
    res += synonyms_dict['adjective']
    res += synonyms_dict['adverb']
    res += synonyms_dict['noun']
    res += synonyms_dict['verb']
  return res

def get_info(word):
  """
  possible affects:  "fear", "anger", "surprise", "negative", "sadness",  etc
  """
  res = {'word': word}
  sense_code, sense = requestWord(word, collection='senselevel')
  intensity_code, intensity = requestWord(word, collection='affectintensity')
  if sense_code == 200:
    # has_sense_data = True
    # print("SENSE:")
    associations = sense['data']['wordlevel'].get('associations', None)
    # pprint(associations)
    res['affect_associations'] = associations
  if intensity_code == 200:
    # has_intensity_data = True
    # print("AFFECT INTENSITY:")
    intensity_data = intensity['data']['affectlist']
    # pprint(intensity_data)
    res['affect_intensity'] = intensity_data
  return res

def get_sad_score(word):
  res = 0.0
  info = get_info(word)
  if 'affect_associations' in info and info['affect_associations'] is not None:
    # print("\t\tSENSE", info['affect_associations'])
    is_sad = 'sadness' in info['affect_associations']
    if is_sad:
      res += 0.5
  if 'affect_intensity' in info:
    # print("\t\tAFFECT", info['affect_intensity'])
    is_sad = lambda x: x['affectdimension'] == 'sadness'
    matches = next(filter(is_sad, info['affect_intensity']), None)
    if matches is not None:
      res += (0.5 * float(matches['score']))
  return res

def get_all_scores(word):
  res = {
    'sadness': 0.0,
    'joy': 0.0,
    'fear': 0.0,
    'anger': 0.0,
  }
  info = get_info(word)
  if 'affect_associations' in info and info['affect_associations'] is not None:
    for affect_dimension in res.keys():
      has_affect = affect_dimension in info['affect_associations']
      if has_affect:
        res[affect_dimension] += 0.5
  if 'affect_intensity' in info:
    for affect_dimension in res.keys():
      has_affect = lambda x: x['affectdimension'] == affect_dimension
      matches = next(filter(has_affect, info['affect_intensity']), None)
      if matches is not None:
        res[affect_dimension] += (0.5 * float(matches['score']))
  return res

def make_sad(body):
  original = body[:]
  for word in list(set(body.split())):
    if word not in stopwords:
      scores = [get_sad_score(word)]
      synonyms = get_synonyms(word)
      words = [word]
      if synonyms:
        words += synonyms
        for synonym in synonyms:
          scores.append(get_sad_score(synonym))
      replacement = words[np.argmax(scores)] if max(scores) != 0.0 else word
      print(word, replacement, scores)
      original = original.replace(word, replacement)
  print(original)

def get_sad_score_body(body):
  words = list(set(body.split()))
  words = list(filter(lambda x: x not in stopwords, words))
  return sum([get_sad_score(word) for word in words]) / len(words)

def score_body(body):
  res = {
    'sadness': 0.0,
    'joy': 0.0,
    'fear': 0.0,
    'anger': 0.0,
  }
  words = list(set(body.split()))
  words = list(filter(lambda x: x not in stopwords, words))
  scores = [get_all_scores(word) for word in words]
  # print(scores)
  for dimension in res.keys():
    for score in scores:
      res[dimension] += score[dimension]
    res[dimension] /= len(words)
  return res
      

if __name__ == "__main__":
  # get_info(sys.argv[1])
  # get_synonyms(sys.argv[1])
  # print(get_sad_score(sys.argv[1]))
  # make_sad("and the poor fool was hanged no no no life why should a dog a horse a rat have life and thou no breath at all thoult come no more never never never never never do you see this look on her look her lips look there look there")
  # make_sad("I had the most wonderful day today the sun was shining and the birds were chirping and love was in the air")
  # print(get_sad_score_body("and the miserable victim was rot no no no sentence why should a dog a horse a betray have sentence and thou no breath at all thoult fall no more never never never never never do you see this lie on her lie her lips lie there lie there"))
  # print(get_sad_score_body("and the poor fool was hanged no no no life why should a dog a horse a rat have life and thou no breath at all thoult come no more never never never never never do you see this look on her look her lips look there look there"))
  # print(get_sad_score_body("I had the most terrific day today the lie was shining and the cry were sing and hate was in the music"))
  # print(get_sad_score_body("I had the most wonderful day today the sun was shining and the birds were chirping and love was in the air"))
  # pprint(score_body("I had the most wonderful day today the sun was shining and the birds were chirping and love was in the air"))
  print(get_sad_score_body("sad depressed and the poor fool was hanged no no no life why should a dog a horse a rat have life and thou no breath at all thoult come no more never never never never never do you see this look on her look her lips look there look there"))
  pprint(score_body("sad depressed and the poor fool was hanged no no no life why should a dog a horse a rat have life and thou no breath at all thoult come no more never never never never never do you see this look on her look her lips look there look there"))

  # check_keys()