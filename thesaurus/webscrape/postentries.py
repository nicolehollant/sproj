import os
import urllib3
import requests 
import json
from pprint import pprint

url = os.getenv("SPROJBASE")+"/thesaurus/api/v1/admin/words"
url = "http://localhost:3000/thesaurus/api/v1/admin/words"
thesaurusLoc = './thesaurus/final/thesaurus-final.json'
testThesaurus = './thesaurus/thesaurus-small.json'
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
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            print(response.text)