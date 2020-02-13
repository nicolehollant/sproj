import os
import json
import urllib3
import requests 
import random
from model.models.model import Model

class Score(Model):

  def __init__(self, prob=None, ignoreArticles=None, collection="words/", debug=False):
    super().__init__(ignoreArticles, collection, debug)
    self.debug = False
    print(f"ignore: {self.ignoreArticles}")

  def selectEntry(self, entry):
    synonyms = self.aggregateWords(entry)
    if synonyms:
      return synonyms[random.randint(0, len(synonyms)-1)]
    return

  def get_synonyms(self, word):
    res = []
    code, thesaurus_response = self.requestWord(word, 'words')
    if code == 200:
      synonyms_dict = thesaurus_response['data']['synonyms']
      res += synonyms_dict['adjective']
      res += synonyms_dict['adverb']
      res += synonyms_dict['noun']
      res += synonyms_dict['verb']
    return res

  def get_info(self, word):
    """
    possible affects:  "fear", "anger", "surprise", "negative", "sadness",  etc
    """
    res = { 'word': word }
    sense_code, sense = self.requestWord(word, collection='senselevel')
    intensity_code, intensity = self.requestWord(word, collection='affectintensity')
    if sense_code == 200:
      associations = sense['data']['wordlevel'].get('associations', None)
      res['affect_associations'] = associations
    if intensity_code == 200:
      intensity_data = intensity['data']['affectlist']
      res['affect_intensity'] = intensity_data
    return res

  def aggregateWords(self, data, mode='synonyms'):
      nyms = []
      for entry in data[mode]:
        currentSection = data[mode][entry]
        for currentWord in currentSection: 
          if currentWord not in nyms:
            nyms.append(currentWord)
      return nyms

  def get_all_scores(self, word):
    res = {
      'sadness': 0.0,
      'joy': 0.0,
      'fear': 0.0,
      'anger': 0.0,
    }
    info = self.get_info(self.stripPunctuation(word))
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

  def score_body(self, body):
    res = {
      'sadness': 0.0,
      'joy': 0.0,
      'fear': 0.0,
      'anger': 0.0,
    }
    words = list(set(body.split()))
    words = list(filter(lambda x: x not in self.articles, words))
    if len(words) == 0:
      return {
        "error": "No valid words"
      }
    scores = [self.get_all_scores(word) for word in words]
    for dimension in res.keys():
      for score in scores:
        res[dimension] += score[dimension]
      res[dimension] /= len(words)
    return res