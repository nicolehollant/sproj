import os
import string
import json
import urllib3
import requests 
import random
from model.config import stopwords

class Model:

    def __init__(self, ignoreArticles=None, collection="words/", debug=False):
        self.baseurl = 'https://sproj.api.colehollant.com/thesaurus/api/v1/'
        self.ignoreArticles = ignoreArticles if ignoreArticles is not None else True
        self.articles = stopwords
        self.debug = debug

    def entryExists(self, word, collection='senselevel'):
        word = word.strip().lower()
        if not word:
            if self.debug:
                print("Word is empty")
            return False, word, {}
        if self.ignoreArticles and word in self.articles:
            if self.debug:
                print("Ignoring article")
            return False, word, {}
        code, response = self.requestWord(word, collection)
        if code != 200: # we've got an error!
            if self.debug:
                print("Not present in db:", word)
            return False, word, {}
        return True, word, response['data']

    def cleanInput(self, text):
        return text

    def stripPunctuation(self, word):
        return word.translate(str.maketrans('', '', string.punctuation))

    def replaceWordPunctuation(self, originalWord, newWord):
        originalStripped = self.stripPunctuation(originalWord).lower()
        return originalWord.replace(originalStripped, newWord.lower())
        
    def requestWord(self, word, collection='senselevel'):
        headers = {
            'Content-Type': 'application/json', 
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
        }
        url = self.baseurl + collection + '/' + word
        response = requests.get(url, headers=headers)
        return response.status_code, response.json()
    