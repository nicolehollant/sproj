import math
import random
import urllib3
import requests 
import json
from pprint import pprint

def radio_score():
  res = [
    '<div class="question">How natural did the above passage sound?</div>'
  ]
  res += ['<div class="question__wrapper"><div class="natural"></div><div>1</div>']
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
    res += [f'<div class="question__wrapper"><div class="subquestion">{question}</div><div>1</div>']
    res += [f'<div class="circ"></div>' for i in range(10)]
    res += ['<div>10</div></div>']
  return res

def make_form(form_type="control"):
  res = [
'''<style>
.natural {
  width: 119px;
}
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
  border: 1px solid #777;
  background: #eee;
  margin: 0 0.5rem;
}
.question {
  font-size: 12px;
  margin: 0.5rem 1rem 0.5rem;
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
.question__wrapper {
  display: flex; 
  align-items: center;
  font-size: 10px;
}
.instructions {
  font-size: 12px;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #888;
}
h2 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
</style>'''
  ]
  with open('./output.json', 'r') as f:
    data = json.load(f)
    # choice control experimental sentence
    # res += [
    #   '<h2>Instructions:</h2>',
    #   '<div class="instructions"><i>Please read each sentence and fill in one circle for each score category</i></div>'
    # ]
    # for i, entry in enumerate(data):
    #   res += [
    #     '<div class="hidden">Unaltered</div>',
    #     f'<div class="prompt">{i + 1}. {entry["sentence"]}</div>',
    #   ]
    #   res += radio_score()
    res += [
      '<h2>Instructions:</h2>',
      '<div class="instructions"><i>Please read each sentence and fill in one circle for each score category</i></div>'
    ]
    random.shuffle(data)
    for i, entry in enumerate(data):
      res += [
        f'<div class="hidden">Altered: {entry["choice"]}</div>',
        f'<div class="prompt">{i + 1}. {entry[form_type]}</div>',
      ]
      res += radio_score()
  return res

if __name__ == "__main__":
  for line in make_form("experimental"):
    print(line)