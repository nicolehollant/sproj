import json
from pprint import pprint


def mean_valence(fname):
  vad = None
  with open('./NRC-VAD-Lexicon/out/vad.json', 'r') as f:
    vad = json.load(f)
  score = {
    "arousal": 0.0,
    "dominance": 0.0,
    "valence": 0.0,
    "num": 0
  }
  with open(fname, 'r') as f:
    words = f.read().split()
    for word in words:
      if word in vad:
        score["arousal"] += float(vad[word]["arousal"])
        score["dominance"] += float(vad[word]["dominance"])
        score["valence"] += float(vad[word]["valence"])
        score["num"] += 1
  score["arousal"] = round(score["arousal"] / score["num"], 5)
  score["dominance"] = round(score["dominance"] / score["num"], 5)
  score["valence"] = round(score["valence"] / score["num"], 5)
  return score

def mode_colour(fname):
  colors = None
  with open('./NRC-Colour-Lexicon/out/colour.json', 'r') as f:
    colors = json.load(f)
  score = {}
  with open(fname, 'r') as f:
    words = f.read().split()
    for word in words:
      if word in colors:
        for sense in colors[word]:
          score[sense["color"]] = score.get(sense["color"], 0) + 1
  return sorted(score.items(), key=lambda a: a[1], reverse=True)

def test_affect_valence():
  print("ANGER:")
  pprint(mean_valence('TESTOUTPUTANGER'))
  print("FEAR:")
  pprint(mean_valence('TESTOUTPUTFEAR'))
  print("JOY:")
  pprint(mean_valence('TESTOUTPUTJOY'))
  print("SADNESS:")
  pprint(mean_valence('TESTOUTPUTSADNESS'))


def test_mode_color():
  print("ANGER:")
  pprint(mode_colour('TESTOUTPUTANGER'))
  # Anger: black, red, gray
  print("FEAR:")
  pprint(mode_colour('TESTOUTPUTFEAR'))
  # Fear: black, red, grey
  print("JOY:")
  pprint(mode_colour('TESTOUTPUTJOY'))
  # Joy: white, yellow, pink
  print("SADNESS:")
  pprint(mode_colour('TESTOUTPUTSADNESS'))
  # Sadness: black, grey, red

if __name__ == "__main__":
  # test_affect_valence()
  test_mode_color()