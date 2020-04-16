import json

def write(dset, filename="words_by_affect.json", append=False):
  with open(filename, 'a' if append else 'w') as outfile:
    json.dump(dset, outfile, sort_keys = True, indent = 2)


def run():
  affect_intensity = json.load(open('./affect_intensity_by_affect.json', 'r'))
  senselevel = json.load(open('./senselevel_by_affect.json', 'r'))
  dataset = {
    'anger': affect_intensity['anger'],
    'fear': affect_intensity['fear'],
    'sadness': affect_intensity['sadness'],
    'joy': affect_intensity['joy'],
  }
  dataset['anger'] += senselevel['anger']
  dataset['fear'] += senselevel['fear']
  dataset['sadness'] += senselevel['sadness']
  dataset['joy'] += senselevel['joy']
  
  dataset['anger'] = list(set(dataset['anger']))
  dataset['fear'] = list(set(dataset['fear']))
  dataset['sadness'] = list(set(dataset['sadness']))
  dataset['joy'] = list(set(dataset['joy']))

  write(dataset)

if __name__ == "__main__":
  run()