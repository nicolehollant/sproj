import os
import urllib3
import requests 
import json
from pprint import pprint
# Started at 1:20pm
url = os.getenv("SPROJBASE")+"/thesaurus/api/v1/admin/"
# url = "http://localhost:3000/thesaurus/api/v1/admin/"

thesaurusLoc = './thesaurus/final/thesaurus-final.json'
testThesaurus = './thesaurus/thesaurus-small.json'

senselevelLoc = '../../db/NRC-Emotion-Lexicon/senselevel/out/senselevel.json'
affectIntensityLoc = '../../db/NRC-Affect-Intensity-Lexicon/out/affect_intensity.json'
colorLoc = '../../db/NRC-Colour-Lexicon/out/colour.json'
vadLoc = '../../db/NRC-VAD-Lexicon/out/vad.json'

def logResponse(endpoint, count, response, word):
    if count % 50 == 0:
        print(endpoint, word, response)

def postThesaurus():
    count = 0
    seen_word = False
    with open(thesaurusLoc) as f:
        data = json.load(f)
        for entry in data:
            count += 1
            if entry == 'aztlan':
                seen_word = True

            if seen_word:
                
                payload = {
                    "word": entry,
                    "synonyms": data[entry]["synonyms"],
                    "antonyms": data[entry]["antonyms"]
                }

                headers = {
                    'Content-Type': 'application/json', 
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
                    'adminUsername': 'cole',
                    'adminPassword': 'cool'
                }
                response = requests.post(url + "words", headers=headers, data=json.dumps(payload))
                logResponse("Thesaurus:", count, response.text, entry)

def postSenseLevel():
    count = 0
    with open(senselevelLoc) as f:
        data = json.load(f)
        for entry in data:
            count += 1

            # POST LIKE THIS
            # "word": "testword",
            # "senselist": [ 
            #     { "sense": [ "lorem", "ipsum" ], "associations": [ "dolor", "sit" ] },
            #     { "sense": [ "consectetur" ], "associations": [ "adipiscing", "elit" ] }
            # ]

            # # PARSE FROM THIS
            # "abandoned": [
            #     { "associations": [ "fear", "negative", "sadness" ], "sense": [ "seclusion" ], "word": "abandoned" },
            #     { "associations": [ "fear", "anger", "negative", "sadness" ], "sense": [ "neglect" ], "word": "abandoned" }
            # ]

            # {
            #     'word': 'force',
            #     'senselist': [
            #         {'associations': [], 'sense': ['motive', 'enforce', 'prick']},
            #         {'associations': ['fear', 'anger', 'negative'], 'sense': ['violence', 'exasperation', 'shock']}]}

            # senselist = []
            for i, _ in enumerate(data[entry]):
                data[entry][i].pop("word")
            payload = {
                "word": entry,
                "senselist": data[entry]
            }
            # pprint(payload)
            headers = {
                'Content-Type': 'application/json', 
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
                'adminUsername': 'cole',
                'adminPassword': 'cool'
            }
            response = requests.post(url + "senselevel", headers=headers, data=json.dumps(payload))
            logResponse("SenseLevel:", count, response.text, entry)

def postaffectintensity():
    count = 0
    with open(affectIntensityLoc) as f:
        data = json.load(f)
        for entry in data:
            count += 1
            # POST LIKE THIS
            # {
            #     "word": "abandon",
            #     "affectlist": [
            #         {
            #           "affectdimension": "fear",
            #           "score": "0.531"
            #         },
            #         {
            #           "affectdimension": "sadness",
            #           "score": "0.703"
            #         }
            #     ]
            # }

            # # PARSE FROM THIS
            # "abandon": [
            #     { "affect_dimension": "fear", "score": "0.531", "word": "abandon" },
            #     { "affect_dimension": "sadness", "score": "0.703", "word": "abandon" }
            #   ]

            for i, _ in enumerate(data[entry]):
                data[entry][i].pop("word")
                data[entry][i]['affectdimension'] = data[entry][i].pop('affect_dimension')
            payload = {
                "word": entry,
                "affectlist": data[entry]
            }
            # pprint(payload)
            headers = {
                'Content-Type': 'application/json', 
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
                'adminUsername': 'cole',
                'adminPassword': 'cool'
            }
            response = requests.post(url + "affectintensity", headers=headers, data=json.dumps(payload))
            logResponse("AffectIntensity:", count, response.text, entry)

def postcolor():
    count = 0
    with open(colorLoc) as f:
        data = json.load(f)
        for entry in data:
            count += 1
            # POST LIKE THIS
            # {
            #     "word": "abandoned",
            #     "colorlist": [
            #         { "color": "black", "sense": [ "seclusion" ], "totalvotes": "10", "votes": "3" },
            #         { "color": "grey", "sense": [ "seclusion" ], "totalvotes": "10", "votes": "3" },
            #         { "color": "black", "sense": [ "neglect" ], "totalvotes": "9", "votes": "6" }
            #     ]
            # }

            # # PARSE FROM THIS
            # "abandoned": [
            #     { "color": "black", "sense": [ "seclusion" ], "totalvotes": "10", "votes": "3", "word": "abandoned" },
            #     { "color": "grey", "sense": [ "seclusion" ], "totalvotes": "10", "votes": "3", "word": "abandoned" },
            #     { "color": "black", "sense": [ "neglect" ], "totalvotes": "9", "votes": "6", "word": "abandoned" }
            #   ],

            for i, _ in enumerate(data[entry]):
                data[entry][i].pop("word")
            payload = {
                "word": entry,
                "colorlist": data[entry]
            }
            # pprint(payload)
            headers = {
                'Content-Type': 'application/json', 
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
                'adminUsername': 'cole',
                'adminPassword': 'cool'
            }
            response = requests.post(url + "color", headers=headers, data=json.dumps(payload))
            logResponse("Colour:", count, response.text, entry)


def postvad():
    count = 0
    with open(vadLoc) as f:
        data = json.load(f)
        for entry in data:
            count += 1
            # POST LIKE THIS
            # {
            #     "word": "abandoned",
            #     "valence": "0.046",
            #     "arousal": "0.481",
            #     "dominance": "0.131",
            # }

            # # PARSE FROM THIS
            # "abandoned": { "arousal": "0.481", "dominance": "0.130", "valence": "0.046", "word": "abandoned" },

            # for i, _ in enumerate(data[entry]):
            #     data[entry][i].pop("word")
            payload = data[entry]
            # pprint(payload)
            headers = {
                'Content-Type': 'application/json', 
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
                'adminUsername': 'cole',
                'adminPassword': 'cool'
            }
            response = requests.post(url + "vad", headers=headers, data=json.dumps(payload))
            logResponse("VAD:", count, response.text, entry)


def avg_nyms():
    count = 0
    maxNym = ''
    maxNyms = 0
    with open(thesaurusLoc) as f:
        data = json.load(f)
        for entry in data:
            nyms = set()
            for nym_arr in data[entry]['synonyms'].values():
                for nym in nym_arr:
                    nyms.add(nym)
            maxNyms += len(nyms)
            count += 1
    print('AVG NYMS', maxNyms, count, maxNyms / count)

def max_nyms():
    maxNym = ''
    maxNyms = 0
    with open(thesaurusLoc) as f:
        data = json.load(f)
        for entry in data:
            nyms = set()
            for nym_arr in data[entry]['synonyms'].values():
                for nym in nym_arr:
                    nyms.add(nym)
            if len(nyms) > maxNyms:
                maxNyms = len(nyms)
                maxNym = entry
    print('Max NYMS', maxNyms, maxNym)


def median(arr):
    n = len(arr) 
    arr.sort() 
    
    if n % 2 == 0: 
        median1 = arr[n//2] 
        median2 = arr[n//2 - 1] 
        median = (median1 + median2)/2
    else: 
        median = arr[n//2] 
    print("median is", median)

def mode(arr):
    from collections import Counter 
    # list of elements to calculate mode 
    n = len(arr) 
    
    data = Counter(arr) 
    get_mode = dict(data) 
    mode = [k for k, v in get_mode.items() if v == max(list(data.values()))] 
    
    if len(mode) == n: 
        get_mode = "No mode found"
    else: 
        get_mode = "Mode is / are: " + ', '.join(map(str, mode)) 
        
    print(get_mode) 

def median_mode_nyms():
    numSynonyms = {}
    with open(thesaurusLoc) as f:
        data = json.load(f)
        for entry in data:
            nyms = set()
            for nym_arr in data[entry]['synonyms'].values():
                for nym in nym_arr:
                    nyms.add(nym)
            numSynonyms[len(nyms)] = numSynonyms.get(len(nyms), 0) + 1
    print('Dist NYMS')
    median(list(numSynonyms.values()))
    mode(list(numSynonyms.values()))

def min_nyms():
    maxNym = ''
    maxNyms = 1000
    with open(thesaurusLoc) as f:
        data = json.load(f)
        for entry in data:
            nyms = set()
            for nym_arr in data[entry]['synonyms'].values():
                for nym in nym_arr:
                    nyms.add(nym)
            if len(nyms) < maxNyms:
                maxNyms = len(nyms)
                maxNym = entry
    print('Min NYMS', maxNyms, maxNym)

def main():
    postThesaurus()
    postSenseLevel()
    postaffectintensity()
    postcolor()
    postvad()

if __name__ == "__main__":
    main()
    # max_nyms()
    # min_nyms()
    # avg_nyms()
    # median_mode_nyms()
    


    