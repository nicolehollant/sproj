import os
import json
import urllib3
import requests 
import random
from model.models.model import Model

class Control(Model):

  def __init__(self, prob=None, ignoreArticles=None, collection="words/", debug=False):
    super().__init__(ignoreArticles, collection, debug)
    self.prob = prob if prob else 0.4
    self.debug = False
    # print(f"Prob: {self.prob}, ignore: {self.ignoreArticles}")

  def selectEntry(self, entry):
    synonyms = self.aggregateWords(entry)
    if synonyms:
      return synonyms[random.randint(0, len(synonyms)-1)]
    return

  def aggregateWords(self, data, mode='synonyms'):
      nyms = []
      for entry in data[mode]:
        currentSection = data[mode][entry]
        for currentWord in currentSection: 
          if currentWord not in nyms:
            nyms.append(currentWord)
      return nyms

  def replaceWords(self, text):
    text = self.cleanInput(text)
    out = []
    notPresent = set()
    stopwordsSkipped = set()
    numChanged = 0

    for word in text.split():
      changed = False

      noPunctuation = self.stripPunctuation(word)

      if random.random() < self.prob:
        exists, wordStripped, data = self.entryExists(noPunctuation, collection='words')
        if exists:
          newEntry = self.selectEntry(data)
          if newEntry:
            numChanged += 1
            out.append(self.replaceWordPunctuation(word, self.selectEntry(data).lower()))
            changed = True
          else:
            notPresent.add(wordStripped)
        elif wordStripped in self.articles:
          stopwordsSkipped.add(wordStripped)
      if not changed:
        out.append(word)
    return out, list(notPresent), numChanged, list(stopwordsSkipped)