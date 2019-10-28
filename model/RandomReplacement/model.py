import os
import json
import urllib3
import requests 
import random

class Model:

    def __init__(self, prob=0.40, ignoreArticles=True):
        self.baseurl = 'https://sproj.api.colehollant.com/thesaurus/api/v1/words/'
        self.prob = prob
        self.ignoreArticles = ignoreArticles
        self.articles = ['a', 'and', 'the', 'an', 'to', 'is', 'be']
        self.debug = False

    def entryExists(self, word):
        word = word.strip().lower()
        if not word:
            if self.debug:
                print("Word is empty")
            return False, word, {}
        if self.ignoreArticles and word in self.articles:
            if self.debug:
                print("Ignoring article")
            return False, word, {}
        code, response = self.requestWord(word)
        if code != 200: # we've got an error!
            if self.debug:
                print("Not present in db:", word)
            return False, word, {}
        return True, word, response['data']
        
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
        out = []
        notPresent = []
        numChanged = 0
        # minNumChanges = len(text) * self.prob # idk if I care about this

        for word in text.split(' '):
            changed = False
            if random.random() < self.prob:
                exists, wordStripped, data = self.entryExists(word)
                if exists:
                    newEntry = self.selectEntry(data)
                    if newEntry:
                        numChanged += 1
                        out.append(self.selectEntry(data).lower())
                        changed = True
                    else:
                        notPresent.append(wordStripped)
            if not changed:
                out.append(word)
        
        return out, notPresent, numChanged

        
    def requestWord(self, word):
        headers = {
            'Content-Type': 'application/json', 
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
        }
        url = self.baseurl + word
        response = requests.get(url, headers=headers)
        return response.status_code, response.json()
    