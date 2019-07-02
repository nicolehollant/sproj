#/bin/python3

# import urllib3
from bs4 import BeautifulSoup
import requests
import json
import os
import re, string
import sys
from pprint import pprint


class ThesaurusScraper:

    def __init__(self):
        self.words = open('words', 'r').readlines()
        self.allHeaders = []

    '''
        Method to scrape entries by word
        params:
            - word: word to scrape
        returns:
            - result: dictionary containing synonyms and antonyms for [word]
    '''
    def scrapeByWord(self, word):
        url = "https://words.bighugelabs.com/" + word
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        # initialize dictionaries for word-entry contents
        synonyms = {}
        antonyms = {}
        # unpack processed parts of speech into the appropriate dictionaries
        synonyms["adjective"], antonyms["adjective"] = self.processSection("adjective", soup)
        synonyms["adverb"], antonyms["adverb"] = self.processSection("adverb", soup)
        synonyms["noun"], antonyms["noun"] = self.processSection("noun", soup)
        synonyms["verb"], antonyms["verb"] = self.processSection("verb", soup)
        # store the synonyms and antonyms in a result dictionary
        result = {word: {"synonyms": synonyms, "antonyms": antonyms}}
        # pprint(result, compact=True)
        return result

    '''
        Helper for extracting synonyms and antonyms for a part of speech
        params: 
            - partOfSpeech: a string for which part of speech to process
            - soup: the html page content from bs4
        returns:
            - synonymsList: list of all synonyms found
            - antonymsList: list of all antonyms found
    '''
    def processSection(self, partOfSpeech, soup):
        # initialize lists for returns
        synonymsList = []
        antonymsList = []
        # look for contents under this part of speech
        thisSection = soup.find("h3", text=partOfSpeech)
        if thisSection:
            # look for the next section (part of speech or other section)
            nextSection = thisSection.findNext("h3")
            # look for antonyms section
            antonyms = thisSection.findNext("h4", text="antonyms")
            if nextSection:
                if antonyms:
                    antonymsUL = antonyms.findNext("ul")
                    nextAntonynms = nextSection.findNext("h4", text="antonyms")
                    # check that antonyms section belongs to this section, not the next section
                    if (nextAntonynms and nextAntonynms.findNext("ul").text != antonymsUL.text) or not nextAntonynms:
                        # gather all entries under the antonyms
                        curAntonyms = antonymsUL.find_all("li")
                        for antonym in curAntonyms:
                            antonymsList.append(antonym.text.strip())
                # loop over all <ul> in this section, add all contained synonyms and antonyms
                curSection = thisSection
                while curSection.findNext("ul") != nextSection.findNext("ul"):
                    curSection = curSection.findNext("ul")
                    for synonym in curSection.find_all("li"):
                        synonymsList.append(synonym.text.strip())
            else:
                if antonyms:
                    # gather all entries under the antonyms
                    curAntonyms = antonyms.findNext("ul").find_all("li")
                    for antonym in curAntonyms:
                        antonymsList.append(antonym.text.strip())
                # loop over all <ul> in this section, add all contained synonyms and antonyms
                for unorderedList in thisSection.find_all("ul"):
                    for synonym in unorderedList.find_all("li"):
                        synonymsList.append(synonym.text.strip())
            # filter out all antonyms from the synonyms list
            synonymsList = list(filter(lambda a: a not in antonymsList, synonymsList))
        return synonymsList, antonymsList


    '''
        Small helper function to get headers (parts of speech and whatnot)
    '''
    def getHeaders(self, word):
        url = "https://words.bighugelabs.com/" + word
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        for head in soup.find_all("h3"):
            head = head.text.strip()
            if head not in self.allHeaders:
                self.allHeaders.append(head)
                print(head)
    
    '''
        Runner that scrapes all words in [self.words]
        Writes to files by first letter
    '''
    def run(self):
        for word in self.words:
            word = word.lower().strip()
            synonyms = self.scrapeByWord(word)
            self.write(synonyms, f"thesaurus/thesaurus-{word[0]}.json", True)
        self.fixJson()
        self.makeThesaurus()

    def write(self, artist, filename, append=False):
        with open(filename, 'a' if append else 'w') as outfile:
            json.dump(artist, outfile, sort_keys = True, indent = 4)


    def fixJson(self):
        directory = os.scandir('./thesaurus')
        for filename in directory:
            if filename.is_file():
                if filename.name.endswith('json'):
                    filestr = ""
                    with open('./thesaurus/'+filename.name, "r") as f:
                        filestr = f.read().replace("}{", "},{")
                    with open('./thesaurus/'+filename.name, "w") as f:
                        f.write("[\n" + filestr + "\n]")

    def makeThesaurus(self):
        directory = os.scandir('./thesaurus')
        thesaurus = {}
        '''
            {
                "word": {
                    "adjective": {
                        "synonyms": ["one", "two",...],
                        "antonyms": ["one", "two",...]
                    },
                    ...
                }
            }
        '''
        for filename in directory:
            if filename.is_file():
                if filename.name.endswith('json') and filename.name.startswith("thesaurus"):
                    filestr = ""
                    with open('./thesaurus/'+filename.name, "r") as f:
                        currentList = json.load(f)
                        for entry in currentList:
                            word = list(entry.keys())[0]
                            if word not in thesaurus:
                                thesaurus.update(entry)
        with open('./thesaurus/final/thesaurus-final.json', "w") as f:
            json.dump(thesaurus, f, indent=2, sort_keys=True)


if __name__ == "__main__":
    scraper = ThesaurusScraper()
    # scraper.run()
    scraper.makeThesaurus()
    