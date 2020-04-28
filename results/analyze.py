from collections import Counter 
import csv
from pprint import pprint
import json
import requests
import math

def countFreq(arr):
  unique = {}
  for val in arr:
    unique[val] = unique.get(val, 0) + 1
  convertToInts = lambda strlist: [int(el) for el in strlist] 
  return convertToInts(list(unique.keys())), list(unique.values())

def stats(data):
  """
  computational formula for sum of deviation scores
  params:
  - data: array of data
  
  returns:
  - ss: sum of squares
  - var: variance
  - std_dev: standard deviation
  """
  data = list(map(abs, data))
  _, freqs = countFreq(data)
  n = sum(freqs)
  ss = sum([x**2 for x in data]) - ((sum(data) ** 2)/n)
  var = ss/(n - 1)
  std_dev = math.sqrt(var)
  mean = sum(data) / n
  return mean, std_dev

def median(arr):
  n = len(arr) 
  arr = list(map(int, arr))
  arr.sort() 
  
  if n % 2 == 0: 
    median1 = arr[n//2] 
    median2 = arr[n//2 - 1] 
    median = (median1 + median2)/2
  else: 
    median = arr[n//2]
  return median

def mode(arr):
  data = Counter(arr) 
  mode = [k for k, v in dict(data).items() if v == max(list(data.values()))] 
  return mode

def score_prompt(rows, i):
  scores = { 
    'natural': 0, 
    'angry': 0, 
    'sad': 0,
    'joy': 0,
    'fear': 0,
    'NUM': 0,
    'count_natural': [],
    'count_angry': [],
    'count_sad': [],
    'count_joy': [],
    'count_fear': [],
  }
  def to_ints(score):
    res = []
    for s in score:
      try:
        res.append(int(s))
      except:
        res.append(None)
    return res

  for score in rows:
    cleaned = to_ints(score)
    if cleaned[i]:
      scores['natural'] += cleaned[i]
      scores['count_natural'].append(cleaned[i])
    if cleaned[i + 1]:
      scores['angry'] += cleaned[i + 1]
      scores['count_angry'].append(cleaned[i + 1])
    if cleaned[i + 2]:
      scores['sad'] += cleaned[i + 2]
      scores['count_sad'].append(cleaned[i + 2])
    if cleaned[i + 3]:
      scores['joy'] += cleaned[i + 3]
      scores['count_joy'].append(cleaned[i + 3])
    if cleaned[i + 4]:
      scores['fear'] += cleaned[i + 4]
      scores['count_fear'].append(cleaned[i + 4])
    scores['NUM'] += 1
  stats = {}
  stats['means'] = {
    'natural': scores['natural'] / scores['NUM'], 
    'angry': scores['angry'] / scores['NUM'], 
    'sad': scores['sad'] / scores['NUM'],
    'joy': scores['joy'] / scores['NUM'],
    'fear': scores['fear'] / scores['NUM'],
  }
  stats['medians'] = {
    'natural': median(scores['count_natural']),
    'angry': median(scores['count_angry']),
    'sad': median(scores['count_sad']),
    'joy': median(scores['count_joy']),
    'fear': median(scores['count_fear']),
  }
  stats['modes'] = {
    'natural': mode(scores['count_natural']),
    'angry': mode(scores['count_angry']),
    'sad': mode(scores['count_sad']),
    'joy': mode(scores['count_joy']),
    'fear': mode(scores['count_fear']),
  }
  stats['data'] = scores
  pprint(stats)
  return stats


def extract_scores(row):
  return row[5:]

def read_file(fname, questions_fname, outfile):
  questions = None
  res = []
  with open(questions_fname, 'r') as f:
    questions = f.readlines()

  with open(fname, 'r') as f:
    fields, *rows = csv.reader(f)
    fields = extract_scores(fields)
    rows = list(map(extract_scores, rows))
    question_ind = 0
    for i in range(len(fields)):
      if i % 5 == 0:
        res.append({
          'question': questions[question_ind],
          'scores': score_prompt(rows, i)
        })
        question_ind += 1
  with open(outfile, 'w') as f:
    json.dump(res, f, indent=2)

def get_model_scores(infile, outfile):
  res = []
  with open(infile, 'r') as f:
    for line in f.readlines():
      line = ".".join(line.split('.')[1:]).strip()
      headers = {'Content-Type': 'application/json'}
      response_raw = requests.post(
        'https://sproj.model.colehollant.com/score', 
        headers=headers, 
        data=json.dumps({
        "text": line,
        "ignore": True
      }))
      response_lda = requests.post(
        'https://sproj.model.colehollant.com/lda', 
        headers=headers, 
        data=json.dumps({
        "text": line,
        "threshold": 0.01,
        "num_keywords": 10
      }))
      res.append({
        'prompt': line,
        'lda': {
          'input': response_lda.json()['data']['net_scores']['input'],
          'topic': response_lda.json()['data']['net_scores']['topic'],
        },
        'raw': response_raw.json()['data']
      })
  with open(outfile, 'w') as f:
    json.dump(res, f)

def average_control_groups():
  with open('results-a.json', 'r') as f:
    results_a = json.load(f)
  with open('results-b.json', 'r') as f:
    results_b = json.load(f)
  for i in range(len(results_a)):
    if results_a[i]['group'] == 'neutral':
      res = {
        'natural': (results_a[i]['scores']['means']['natural'] + results_b[i]['scores']['means']['natural']) / 2,
        'angry': (results_a[i]['scores']['means']['angry'] + results_b[i]['scores']['means']['angry']) / 2,
        'sad': (results_a[i]['scores']['means']['sad'] + results_b[i]['scores']['means']['sad']) / 2,
        'joy': (results_a[i]['scores']['means']['joy'] + results_b[i]['scores']['means']['joy']) / 2,
        'fear': (results_a[i]['scores']['means']['fear'] + results_b[i]['scores']['means']['fear']) / 2,
      }
      results_b[i]['scores'] = res
    else:
      results_b[i]['scores'] = results_b[i]['scores']['means']
  with open('results-combined.json', 'w') as f:
    json.dump(results_b, f)

def find_corresponding(prompt, scores):
  for entry in scores:
    if prompt == entry['prompt']:
      return entry
  return None

def combine_results():
  with open('results-combined.json', 'r') as f:
    results_combined = json.load(f)
  with open('scores-combined.json', 'r') as f:
    scores_combined = json.load(f)
  for i in range(len(results_combined)):
    corresponding = find_corresponding(results_combined[i]['question'], scores_combined)
    if not corresponding:
      print("hmmmmmm", results_combined[i]['question'])
      exit(-1)
    results_combined[i]['scores'] = {
      'real': results_combined[i]['scores'],
      'lda': corresponding['lda'],
      'raw': corresponding['raw'],
    }
  with open('results-final.json', 'w') as f:
    json.dump(results_combined, f)
  
def error(observed, expected):
  return (observed - expected) / expected

def error_group(group, real):
  return {
    'anger': error(group['anger'], real['angry'] / 10),
    'sadness': error(group['sadness'], real['sad'] / 10),
    'joy': error(group['joy'], real['joy'] / 10),
    'fear': error(group['fear'], real['fear'] / 10),
  }

def print_row(question, group, target, natural, anger_error, sadness_error, joy_error, fear_error):
  print('| ', ' | '.join(list(map(str, [question, group, target, natural, anger_error, sadness_error, joy_error, fear_error]))), ' |')

def print_row_two(anger_error, sadness_error, joy_error, fear_error):
  print('| ', ' | '.join(list(map(str, [anger_error, sadness_error, joy_error, fear_error]))), ' |')

def print_row_three(group, target, anger_error, sadness_error, joy_error, fear_error, mean_error, stddev):
  print('| ', ' | '.join(list(map(str, [group, target, anger_error, sadness_error, joy_error, fear_error, mean_error, stddev]))), ' |')

def results_error_full():
  with open('results-final.json', 'r') as f:
    results = json.load(f)
  for category in ['error_lda_input', 'error_lda_topic', 'error_raw']:
    print('\n', '**{}**'.format(category), '\n')
    print('| question | group | target | natural | anger error | sadness error | joy error | fear error |')
    print('| --- | --- | --- | --- | --- | --- | --- | --- |')
    for i in range(len(results)):
      res = {
        'error_lda_input': error_group(results[i]['scores']['lda']['input'], results[i]['scores']['real']),
        'error_lda_topic': error_group(results[i]['scores']['lda']['topic'], results[i]['scores']['real']),
        'error_raw': error_group(results[i]['scores']['raw'], results[i]['scores']['real']),
      }
      print_row(
        results[i]['question'], 
        results[i]['group'], 
        results[i]['target'], 
        round(results[i]['scores']['real']['natural'] / 10, 5),
        round(res[category]['anger'], 5),
        round(res[category]['sadness'], 5),
        round(res[category]['fear'], 5),
        round(res[category]['joy'], 5),
      )

def results_error_mean_total():
  with open('results-final.json', 'r') as f:
    results = json.load(f)
  for category in ['error_lda_input', 'error_lda_topic', 'error_raw']:
    print('\n', '**{}**'.format(category), '\n')
    print('| anger error | sadness error | joy error | fear error |')
    print('| --- | --- | --- | --- |')
    res = {
      'anger': 0.0,
      'sadness': 0.0,
      'fear': 0.0,
      'joy': 0.0,
      'NUM': 0
    }
    for i in range(len(results)):
      # turned out I wasn't normalizing by input size
      results[i]['scores']['lda']['input']['anger'] *= (1487 / len(results[i]['question'].split()))
      results[i]['scores']['lda']['input']['sadness'] *= (1302 / len(results[i]['question'].split()))
      results[i]['scores']['lda']['input']['fear'] *= (1772 / len(results[i]['question'].split()))
      results[i]['scores']['lda']['input']['joy'] *= (1269 / len(results[i]['question'].split()))
      curr = {
        'error_lda_input': error_group(results[i]['scores']['lda']['input'], results[i]['scores']['real']),
        'error_lda_topic': error_group(results[i]['scores']['lda']['topic'], results[i]['scores']['real']),
        'error_raw': error_group(results[i]['scores']['raw'], results[i]['scores']['real']),
      }
      res['anger'] += curr[category]['anger']
      res['sadness'] += curr[category]['sadness']
      res['fear'] += curr[category]['fear']
      res['joy'] += curr[category]['joy']
      res['NUM'] += 1
    print_row_two(
      round(res['anger'] / res['NUM'], 5),
      round(res['sadness'] / res['NUM'], 5),
      round(res['fear'] / res['NUM'], 5),
      round(res['joy'] / res['NUM'], 5),
    )

def results_error_mean_grouped():
  with open('results-final.json', 'r') as f:
    results = json.load(f)
  for category in ['error_lda_input', 'error_lda_topic', 'error_raw']:
    res_control = {'anger': 0.0, 'sadness': 0.0, 'fear': 0.0, 'joy': 0.0, 'NUM': 0}
    res_neutral = {'anger': 0.0, 'sadness': 0.0, 'fear': 0.0, 'joy': 0.0, 'NUM': 0}
    res_exp = {}
    res_exp['anger'] = {'anger': 0.0, 'sadness': 0.0, 'fear': 0.0, 'joy': 0.0, 'NUM': 0}
    res_exp['sadness'] = {'anger': 0.0, 'sadness': 0.0, 'fear': 0.0, 'joy': 0.0, 'NUM': 0}
    res_exp['joy'] = {'anger': 0.0, 'sadness': 0.0, 'fear': 0.0, 'joy': 0.0, 'NUM': 0}
    res_exp['fear'] = {'anger': 0.0, 'sadness': 0.0, 'fear': 0.0, 'joy': 0.0, 'NUM': 0}
    for i in range(len(results)):
      # turned out I wasn't normalizing by input size
      results[i]['scores']['lda']['input']['anger'] *= (1487 / len(results[i]['question'].split()))
      results[i]['scores']['lda']['input']['sadness'] *= (1302 / len(results[i]['question'].split()))
      results[i]['scores']['lda']['input']['fear'] *= (1772 / len(results[i]['question'].split()))
      results[i]['scores']['lda']['input']['joy'] *= (1269 / len(results[i]['question'].split()))
      curr = {
        'error_lda_input': error_group(results[i]['scores']['lda']['input'], results[i]['scores']['real']),
        'error_lda_topic': error_group(results[i]['scores']['lda']['topic'], results[i]['scores']['real']),
        'error_raw': error_group(results[i]['scores']['raw'], results[i]['scores']['real']),
      }
      if results[i]['group'] == 'neutral':
        res_neutral['anger'] += curr[category]['anger']
        res_neutral['sadness'] += curr[category]['sadness']
        res_neutral['fear'] += curr[category]['fear']
        res_neutral['joy'] += curr[category]['joy']
        res_neutral['NUM'] += 1
      elif results[i]['group'] == 'control':
        res_control['anger'] += curr[category]['anger']
        res_control['sadness'] += curr[category]['sadness']
        res_control['fear'] += curr[category]['fear']
        res_control['joy'] += curr[category]['joy']
        res_control['NUM'] += 1
      else:
        res_exp[results[i]['target']]['anger'] += curr[category]['anger']
        res_exp[results[i]['target']]['sadness'] += curr[category]['sadness']
        res_exp[results[i]['target']]['fear'] += curr[category]['fear']
        res_exp[results[i]['target']]['joy'] += curr[category]['joy']
        res_exp[results[i]['target']]['NUM'] += 1
    # mean, std_dev = stats()
    print('\n', '**{}**'.format(category), '\n')
    print('| group | target | anger error | sadness error | joy error | fear error | mean abs(error) | std dev |')
    print('| --- | --- | --- | --- | --- | --- | --- | --- |')
    mean, stddev = stats([res_neutral['anger'] / res_neutral['NUM'], res_neutral['sadness'] / res_neutral['NUM'], res_neutral['fear'] / res_neutral['NUM'], res_neutral['joy'] / res_neutral['NUM']])
    print_row_three(
      'neutral',
      '',
      round(res_neutral['anger'] / res_neutral['NUM'], 5),
      round(res_neutral['sadness'] / res_neutral['NUM'], 5),
      round(res_neutral['fear'] / res_neutral['NUM'], 5),
      round(res_neutral['joy'] / res_neutral['NUM'], 5),
      round(mean, 5),
      round(stddev, 5)
    )
    mean, stddev = stats([res_control['anger'] / res_control['NUM'], res_control['sadness'] / res_control['NUM'], res_control['fear'] / res_control['NUM'], res_control['joy'] / res_control['NUM']])
    print_row_three(
      'control',
      '',
      round(res_control['anger'] / res_control['NUM'], 5),
      round(res_control['sadness'] / res_control['NUM'], 5),
      round(res_control['fear'] / res_control['NUM'], 5),
      round(res_control['joy'] / res_control['NUM'], 5),
      round(mean, 5),
      round(stddev, 5)
    )
    mean, stddev = stats([res_exp['anger']['anger'] / res_exp['anger']['NUM'], res_exp['anger']['sadness'] / res_exp['anger']['NUM'], res_exp['anger']['fear'] / res_exp['anger']['NUM'], res_exp['anger']['joy'] / res_exp['anger']['NUM']])
    print_row_three(
      'experimental',
      'anger',
      round(res_exp['anger']['anger'] / res_exp['anger']['NUM'], 5),
      round(res_exp['anger']['sadness'] / res_exp['anger']['NUM'], 5),
      round(res_exp['anger']['fear'] / res_exp['anger']['NUM'], 5),
      round(res_exp['anger']['joy'] / res_exp['anger']['NUM'], 5),
      round(mean, 5),
      round(stddev, 5)
    )
    mean, stddev = stats([res_exp['sadness']['anger'] / res_exp['sadness']['NUM'], res_exp['sadness']['sadness'] / res_exp['sadness']['NUM'], res_exp['sadness']['fear'] / res_exp['sadness']['NUM'], res_exp['sadness']['joy'] / res_exp['sadness']['NUM']])
    print_row_three(
      'experimental',
      'sadness',
      round(res_exp['sadness']['anger'] / res_exp['sadness']['NUM'], 5),
      round(res_exp['sadness']['sadness'] / res_exp['sadness']['NUM'], 5),
      round(res_exp['sadness']['fear'] / res_exp['sadness']['NUM'], 5),
      round(res_exp['sadness']['joy'] / res_exp['sadness']['NUM'], 5),
      round(mean, 5),
      round(stddev, 5)
    )
    mean, stddev = stats([res_exp['joy']['anger'] / res_exp['joy']['NUM'], res_exp['joy']['sadness'] / res_exp['joy']['NUM'], res_exp['joy']['fear'] / res_exp['joy']['NUM'], res_exp['joy']['joy'] / res_exp['joy']['NUM']])
    print_row_three(
      'experimental',
      'joy',
      round(res_exp['joy']['anger'] / res_exp['joy']['NUM'], 5),
      round(res_exp['joy']['sadness'] / res_exp['joy']['NUM'], 5),
      round(res_exp['joy']['fear'] / res_exp['joy']['NUM'], 5),
      round(res_exp['joy']['joy'] / res_exp['joy']['NUM'], 5),
      round(mean, 5),
      round(stddev, 5)
    )
    mean, stddev = stats([res_exp['fear']['anger'] / res_exp['fear']['NUM'], res_exp['fear']['sadness'] / res_exp['fear']['NUM'], res_exp['fear']['fear'] / res_exp['fear']['NUM'], res_exp['fear']['joy'] / res_exp['fear']['NUM']])
    print_row_three(
      'experimental',
      'fear',
      round(res_exp['fear']['anger'] / res_exp['fear']['NUM'], 5),
      round(res_exp['fear']['sadness'] / res_exp['fear']['NUM'], 5),
      round(res_exp['fear']['fear'] / res_exp['fear']['NUM'], 5),
      round(res_exp['fear']['joy'] / res_exp['fear']['NUM'], 5),
      round(mean, 5),
      round(stddev, 5)
    )
    

if __name__ == "__main__":
  # read_file('Survey-B.csv', 'questions-b.md', 'res-b.json')
  # read_file('Survey-A.csv', 'questions-a.md', 'res-a.json')
  # indep_samples_t_test()
  # get_model_scores('questions-a.md', 'scores-a.json')
  # get_model_scores('questions-b.md', 'scores-b.json')
  # average_control_groups()
  # combine_results()
  # results_error_mean_total()
  results_error_mean_grouped()