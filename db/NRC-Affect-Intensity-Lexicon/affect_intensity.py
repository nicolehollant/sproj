import json
import os

class AffectIntensity():
  """
  Manipulate the "NRC-Colour-Lexicon" dataset for our use

  FILE FORMAT (from their readme):
    Each line has the following format:
    <Term><tab><Score><tab><AffectDimension>

    <Term> is a word for which the annotations are provided;

    <Score> is the real-valued emotion intensity score;

    <AffectDimension> is one of the emotions (anger, fear, joy, or sadness).


  EX:
    aaaaaaah	0.479	0.606	0.291
  """

  def __init__(self):
    path = "../../resources/NRC-Sentiment-Emotion-Lexicons/NRC-Affect-Intensity-Lexicon/NRC-AffectIntensity-Lexicon.txt"
    self.lines = open(path, 'r').readlines()[1:]
    self.outfile = "out/affect_intensity.json"
    self.dataset = {}

  def process_line(self, line):
    """
    process a line
    
    @params: line -- a line of text as per the file format:
    - <Term><tab><Score><tab><AffectDimension>
   
    @returns: dictionary representing the entry
    """
    sections = line.split('\t')
    return {
      "word": sections[0].strip(),
      "score": sections[1].strip(),
      "affect_dimension": sections[2].strip()
    }

  def run(self):
    """
    Runner that processes all words in [self.lines]
    Writes to files by first letter
    """
    for line in self.lines:
      line = line.lower().strip()
      entry = self.process_line(line)
      self.write(entry, f"tmp/affect_intensity-{entry['word'][0]}.json", True)
    self.fix_json()
    self.make_dataset()

  def fix_json(self):
    directory = os.scandir('./tmp')
    for filename in directory:
      if filename.is_file():
        if filename.name.endswith('json'):
          filestr = ""
          with open('./tmp/'+filename.name, "r") as f:
            filestr = f.read().replace("}{", "},{")
          with open('./tmp/'+filename.name, "w") as f:
            f.write("[\n" + filestr + "\n]")

  def write(self, entry, filename, append=False):
    with open(filename, 'a' if append else 'w') as outfile:
      json.dump(entry, outfile, sort_keys = True, indent = 2)

  def make_dataset(self):
    directory = os.scandir('./tmp')
    dataset = {}
    """
    {
      "<WORD>": {
        "word": <word>,
        "score": <score>,
        "affect-dimension": <affect-dimension>
      }
    }
    """
    for filename in directory:
      if filename.is_file():
        if filename.name.endswith('json') and filename.name.startswith("affect_intensity-"):
          with open('./tmp/'+filename.name, "r") as f:
            currentList = json.load(f)
            for entry in currentList:
              curr = list(dataset.get(entry["word"], []))
              curr.append(entry)
              dataset[entry["word"]] = curr

          os.remove('./tmp/'+filename.name)
    with open(self.outfile, "w") as f:
      json.dump(dataset, f, indent=2, sort_keys=True)
  
if __name__ == "__main__":
  affect_intensity = AffectIntensity()
  affect_intensity.run()