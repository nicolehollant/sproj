import os
import urllib3
import requests 
import json
from pprint import pprint

url = os.getenv("SPROJBASE")+"/thesaurus/api/v1/admin/"
url = "http://localhost:3000/thesaurus/api/v1/admin/"

thesaurusLoc = './thesaurus/final/thesaurus-final.json'
testThesaurus = './thesaurus/thesaurus-small.json'

senselevelLoc = '../../db/NRC-Emotion-Lexicon/senselevel/out/senselevel.json'

def postThesaurus():
    seen_legislate = False
    with open(thesaurusLoc) as f:
        data = json.load(f)
        for entry in data:
            if entry == 'legislate':
                seen_legislate = True

            if seen_legislate:
                
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
                print(response.text)

def postSenseLevel():
    with open(senselevelLoc) as f:
        data = json.load(f)
        for entry in data:


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
            print(response.text)

def postaffectintensity():
    with open(affectintensityLoc) as f:
        data = json.load(f)
        for entry in data:

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
            print(response.text)

def postcolor():
    with open(colorLoc) as f:
        data = json.load(f)
        for entry in data:

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
            print(response.text)


def postvad():
    with open(vadLoc) as f:
        data = json.load(f)
        for entry in data:

            # POST LIKE THIS
            # {
            #     "word": "abandoned",
            #     "valence": "0.046",
            #     "arousal": "0.481",
            #     "dominance": "0.131",
            # }

            # # PARSE FROM THIS
            # "abandoned": { "arousal": "0.481", "dominance": "0.130", "valence": "0.046", "word": "abandoned" },

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
            print(response.text)

if __name__ == "__main__":
    postSenseLevel()