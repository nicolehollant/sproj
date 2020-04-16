import math
import random
import urllib3
import requests 
import json
from pprint import pprint

def score_sentences():

  sentences = [
    "When motorists sped in and out of traffic, all she could think of was those in need of a transplant.",
    "I am my aunt's sister's daughter.",
    "Joyce enjoyed eating pancakes with ketchup.",
    "He drank life before spitting it out.",
    "Never underestimate the willingness of the greedy to throw you under the bus.",
    "The lake is a long way from here.",
    "He excelled at firing people nicely.",
    "The toy brought back fond memories of being lost in the rain forest.",
    "Sometimes you have to just give up and win by cheating.",
    "The blinking lights of the antenna tower came into focus just as I heard a loud snap.",
    "He wasn't bitter that she had moved on but from the radish.",
    "I love bacon, beer, birds, and baboons.",
    "The shooter says goodbye to his love.",
    "Getting up at dawn is for the birds.",
    "The tart lemonade quenched her thirst, but not her longing.",
    "He was surprised that his immense laziness was inspirational to others.",
    "They got there early, and they got really good seats.",
    "You can't compare apples and oranges, but what about bananas and plantains?",
    "He uses onomatopoeia as a weapon of mental destruction.",
    "They say that dogs are man's best friend, but this cat was setting out to sabotage that theory.",
    "Everyone was curious about the large white blimp that appeared overnight.",
    "She found his complete dullness interesting.",
    "Italy is my favorite country; in fact, I plan to spend two weeks there next year.",
    "Peanut butter and jelly caused the elderly lady to think about her past.",
    "We have a lot of rain in June.",
    "He took one look at what was under the table and noped the hell out of there.",
    "He colored deep space a soft yellow.",
    "She advised him to come back at once.",
    "Jeanne wished she has chosen the red button.",
    "This book is sure to liquefy your brain.",
    "I'd rather be a bird than a fish.",
    "The waves were crashing on the shore; it was a lovely sight.",
    "Shakespeare was a famous 17th-century diesel mechanic.",
    "Twin 4-month-olds slept in the shade of the palm tree while the mother tanned in the sun.",
    "Stop waiting for exceptional things to just happen.",
    "She saw the brake lights, but not in time.",
    "Everybody should read Chaucer to improve their everyday vocabulary.",
    "Going from child, to childish, to childlike is only a matter of time.",
    "He was willing to find the depths of the rabbit hole in order to be with her.",
    "When transplanting seedlings, candied teapots will make the task easier.",
  ]

  scores = []

  headers = {
    'Content-Type': 'application/json', 
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'adminUsername': 'cole',
    'adminPassword': 'cool'
  }


  # for sentence in sentences:
  #   payload = {
  #     'text': sentence,
  #     'ignore': True
  #   }
  #   response = requests.post('http://localhost:5000/score', headers=headers, data=json.dumps(payload))
  #   scores.append({
  #     'sentence': sentence,
  #     'data': response.json()['data']
  #   })


  headers = {
    'Content-Type': 'application/json', 
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'adminUsername': 'cole',
    'adminPassword': 'cool'
  }

  nice_ones = [
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
    'He uses onomatopoeia as a weapon of mental destruction.',
    "They say that dogs are man's best friend, but this cat was setting out to sabotage that theory.",
    'She found his complete dullness interesting.',
    'Italy is my favorite country; in fact, I plan to spend two weeks there next year.',
    'Peanut butter and jelly caused the elderly lady to think about her past.',
    'We have a lot of rain in June.',
    'He took one look at what was under the table and noped the hell out of there.',
    'She advised him to come back at once.',
    'He colored deep space a soft yellow.',
    "I'd rather be a bird than a fish.",
    'The waves were crashing on the shore; it was a lovely sight.',
    'Twin 4-month-olds slept in the shade of the palm tree while the mother tanned in the sun.',
    'Stop waiting for exceptional things to just happen.',
    'She saw the brake lights, but not in time.',
    'She was willing to find the depths of the rabbit hole in order to be with her.',
    'When transplanting seedlings, candied teapots will make the task easier.'
    "I am my aunt's sister's daughter.",
    'He excelled at firing people nicely.',
    'Jeanne wished she has chosen the red button.',
    'Never underestimate the willingness of the greedy to throw you under the bus.'
  ]

  # pprint(scores)

  # print(len(nice_ones))
  for sentence in nice_ones:
    payload = {
      'text': sentence,
      'prob': 1,
      'ignore': True
    }
    response = requests.post('http://localhost:5000/control', headers=headers, data=json.dumps(payload))
    scores.append({
      'sentence': sentence,
      'data': response.json()['data']['output']
    })

  pprint(scores)

def random_half(num):
  res = []
  for _ in range(math.floor(num/2)):
    inserted = False
    while not inserted:
      r = random.randint(0, num) 
      if r not in res:
        res.append(r)
        inserted = True
  return res

def radio_score():
  res = [
    '<div class="question">How natural did the above passage sound?</div>'
  ]
  res += ['<div style="display: flex; align-items: center;"><div style="width: 12ch; padding-right: 1rem;"></div><div>1</div>']
  res += [f'<div class="circ"></div>' for i in range(10)]
  res += ['<div>10</div></div>', 
    '</div>',
    '<div class="question">To what extent was the above passage:</div>'
  ]
  questions = [
    '<i>angry?</i>',
    '<i>sad?</i>',
    '<i>joyful?</i>',
    '<i>fearful?</i>',
  ]
  for question in questions:
    res += [f'<div style="display: flex; align-items: center;"><div class="subquestion">{question}</div><div>1</div>']
    res += [f'<div class="circ"></div>' for i in range(10)]
    res += ['<div>10</div></div>']
  return res
  # res = []
  # questions = [
  #   'How natural did the above passage sound?',
  #   'To what extent was the above passage <i>angry?</i>',
  #   'To what extent was the above passage <i>sad?</i>',
  #   'To what extent was the above passage <i>joyful?</i>',
  #   'To what extent was the above passage <i>fearful?</i>',
  # ]
  # for question in questions:
  #   res += [f'<div class="question">{question}</div>']
  #   res += ['<div style="display: flex; align-items: center;"><div>1</div>']
  #   res += [f'<div class="circ"></div>' for i in range(10)]
  #   res += ['<div>10</div></div>', '</div>']
  # return res

def make_form():
  res = [
'''<style>
.hidden { 
  display: none; 
}
.choice {
  width: 2rem;
  text-align: center;
  font-size: 10px;
}
.circ {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 1rem;
  border: 1px solid black;
  background: #eee;
  margin: 0 0.5rem;
}
.question {
  font-size: 12px;
  margin: 1rem 1rem 0.5rem;
}
.prompt {
  font-size: 14px;
  margin: 1rem 0 0;
}
.subquestion {
  font-size: 10px;
  width: 10ch; 
  padding-right: 1rem;
  margin: 0 1.5rem 0.125rem;
}
</style>'''
  ]
  with open('./output.json', 'r') as f:
    data = json.load(f)
    altered_inds = random_half(len(data))
    for i, entry in enumerate(data):
      # how natural the passage sounded, as well as scoring each sentence from 1-10 for the strength of association between the passage and each of the following categories: anger, fear, joy, and sadness.
      if i in altered_inds:
        res += [
          f'<div class="hidden">Altered: {entry["choice"]}</div>',
          f'<div class="prompt">{i + 1}. {entry["data"]}</div>',
        ]
      else:
        res += [
          f'<div class="hidden">Unaltered</div>',
          f'<div class="prompt">{i + 1}. {entry["sentence"]}</div>',
        ]
      res += radio_score()
    # choice
    # data
    # sentence
  return res

if __name__ == "__main__":
  # print(make_form())
  for line in make_form():
    print(line)