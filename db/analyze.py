import random
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

def make_affect(body, affect):
  if affect not in ['sadness', 'joy', 'fear', 'anger']:
    return None
  original = body[:]
  for word in list(set(body.split())):
    if word not in stopwords:
      scores = [get_all_scores(word)[affect]]
      synonyms = get_synonyms(word)
      words = [word]
      if synonyms:
        words += synonyms
        for synonym in synonyms:
          scores.append(get_all_scores(synonym)[affect])
      replacement = words[np.argmax(scores)] if max(scores) != 0.0 else word
      # print(word, replacement, scores)
      original = original.replace(word, replacement)
  # print(original)
  # return {
  #   'original': body,
  #   'altered': original,
  #   'original_score': score_body(body),
  #   'altered_score': score_body(original)
  # }
  return original

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
  # print(get_sad_score_body("sad depressed and the poor fool was hanged no no no life why should a dog a horse a rat have life and thou no breath at all thoult come no more never never never never never do you see this look on her look her lips look there look there"))
  # pprint(score_body("sad depressed and the poor fool was hanged no no no life why should a dog a horse a rat have life and thou no breath at all thoult come no more never never never never never do you see this look on her look her lips look there look there"))
  # body = "I had the most wonderful day today the sun was shining and the birds were chirping and love was in the air"
  # print(make_affect(body, 'fear'))
  # make_sad(body)
  # check_keys()

  # {
  #   'original': 
  #     'I had the most wonderful day today the sun was shining and the birds were chirping and love was in the air', 
  #   'altered': 
  #     'I had the most terrific day today the lie was shining and the cry were sing and hate was in the music', 
  #   'original_score': {
  #     'sadness': 0.0, 'joy': 0.34, 'fear': 0.0, 'anger': 0.0
  #   }, 
  #   'altered_score': {
  #     'sadness': 0.40745000000000003, 'joy': 0.23875000000000002, 'fear': 0.0742, 'anger': 0.1588
  #   }
  # }

  # {
  #   'original': 'I had the most wonderful day today the sun was shining and the birds were chirping and love was in the air', 
  #   'altered': 'I had the most wonderful day today the expose was shining and the outcry were chirping and bang was in the expose', 
  #   'original_score': {'sadness': 0.0, 'joy': 0.34, 'fear': 0.0, 'anger': 0.0}, 
  #   'altered_score': {'sadness': 0.06944444444444445, 'joy': 0.2058888888888889, 'fear': 0.2541111111111111, 'anger': 0.1647777777777778}
  # }


  headers = {
    'Content-Type': 'application/json', 
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
  }

  scores = []

  nice_ones = [
    'When motorists sped in and out of traffic, all she could think of was those in need of a transplant.',
    'He drank life before spitting it out.',
    'The toy brought back fond memories of being lost in the rain forest.',
    'Italy is my favorite country; in fact, I plan to spend two weeks there next year.',
    'The blinking lights of the antenna tower came into focus just as I heard a loud snap.',
    'I love bacon, beer, birds, and baboons.',
    'She saw the brake lights, but not in time.',
    "They say that dogs are man's best friend, but this cat was setting out to sabotage that theory.",
    'The tart lemonade quenched her thirst, but not her longing.',
    'He was surprised that his immense laziness was inspirational to others.',
    'They got there early, and they got really good seats.'
    "You can't compare apples and oranges, but what about bananas and plantains?",
  ]

  all_nice_ones = [
    'When motorists sped in and out of traffic, all she could think of was those in need of a transplant.',
    'He drank life before spitting it out.',
    'The toy brought back fond memories of being lost in the rain forest.',
    'Sometimes you have to just give up and win by cheating.',
    'The blinking lights of the antenna tower came into focus just as I heard a loud snap.',
    'I love bacon, beer, birds, and baboons.',
    'The shooter says goodbye to his love.',
    'Getting up at dawn is for the birds.',
    'The tart lemonade quenched her thirst, but not her longing.',
    'He was surprised that his immense laziness was inspirational to others.',
    'They got there early, and they got really good seats.'
    "You can't compare apples and oranges, but what about bananas and plantains?",
    # 'He uses onomatopoeia as a weapon of mental destruction.',
    # "They say that dogs are man's best friend, but this cat was setting out to sabotage that theory.",
    # 'She found his complete dullness interesting.',
    # 'Italy is my favorite country; in fact, I plan to spend two weeks there next year.',
    # 'Peanut butter and jelly caused the elderly lady to think about her past.',
    # 'We have a lot of rain in June.',
    # 'He took one look at what was under the table and noped the hell out of there.',
    # 'She advised him to come back at once.',
    # 'He colored deep space a soft yellow.',
    # "I'd rather be a bird than a fish.",
    # 'The waves were crashing on the shore; it was a lovely sight.',
    # 'Twin 4-month-olds slept in the shade of the palm tree while the mother tanned in the sun.',
    # 'Stop waiting for exceptional things to just happen.',
    # 'She saw the brake lights, but not in time.',
    # 'She was willing to find the depths of the rabbit hole in order to be with her.',
    # 'When transplanting seedlings, candied teapots will make the task easier.'
    # "I am my aunt's sister's daughter.",
    # 'He excelled at firing people nicely.',
    # 'Jeanne wished she has chosen the red button.',
    # 'Never underestimate the willingness of the greedy to throw you under the bus.'
  ]

  for sentence in ["You can't compare apples and oranges, but what about bananas and plantains?"]:
    choice = random.choice(['sadness', 'joy', 'fear', 'anger'])
    payload = {
      'text': sentence,
      'prob': 1,
      'ignore': True
    }
    response = requests.post('http://localhost:5000/control', headers=headers, data=json.dumps(payload))
    changed = make_affect(sentence, choice)
    scores.append({
      'choice': choice,
      'sentence': sentence,
      'control': response.json()['data']['output'],
      'experimental': changed
    })
  # for sentence in nice_ones:
  #   choice = random.choice(['sadness', 'joy', 'fear', 'anger', 'control'])
  #   if choice == 'control':
  #     payload = {
  #       'text': sentence,
  #       'prob': 1,
  #       'ignore': True
  #     }
  #     response = requests.post('http://localhost:5000/control', headers=headers, data=json.dumps(payload))
  #     scores.append({
  #       'choice': choice,
  #       'sentence': sentence,
  #       'data': response.json()['data']['output']
  #     })
  #   else:
  #     response = make_affect(sentence, choice)
  #     scores.append({
  #       'choice': choice,
  #       'sentence': sentence,
  #       'data': response
  #     })

  with open('output4.json', "w") as f:
    json.dump(scores, f, indent=2, sort_keys=True)
  pprint(scores)