import json
import os

def write(dset, filename="out/affect_intensity_by_affect.json", append=False):
  with open(filename, 'a' if append else 'w') as outfile:
    json.dump(dset, outfile, sort_keys = True, indent = 2)


def run():
  data = json.load(open('./out/affect_intensity.json', 'r'))
  dataset = {
    'anger': [],
    'fear': [],
    'sadness': [],
    'joy': [],
  }

  for word, affect_list in data.items():
    for affect_dimension in dataset.keys():
      if any([entry['affect_dimension'] == affect_dimension for entry in affect_list]):
        dataset[affect_dimension].append(word)
  
  write(dataset)

if __name__ == "__main__":
  run()