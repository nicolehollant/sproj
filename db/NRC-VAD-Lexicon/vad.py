import json
import os

class VAD():
  """
  Manipulate the "NRC-VAD-Lexicon" dataset for our use

  FILE FORMAT (from their readme):
    Annotations at WORD LEVEL (file: NRC-VAD-Lexicon.txt)

    NRC-VAD-Lexicon.txt: This is the main lexicon file with entries for 20,0007 English words. It has four columns
    (separated by tabs):
    - Word: The English word for which V, A, and D scores are provided. The words are listed in alphabetic order.
    - Valence: valence score of the word
    - Arousal: arousal score of the word
    - Dominance: dominance score of the word

  EX:
    aaaaaaah	0.479	0.606	0.291
  """

  def __init__(self):
    path = "../../resources/NRC-Sentiment-Emotion-Lexicons/NRC-VAD-Lexicon/NRC-VAD-Lexicon.txt"
    self.lines = open(path, 'r').readlines()[1:]
    self.outfile = "out/vad.json"
    self.dataset = {}

  def process_line(self, line):
    """
    process a line
    
    @params: line -- a line of text as per the file format:
    - <term><tab><Valence><tab><Arousal><tab><Dominance>
    @returns: 
    - complete: boolean indicating finished state of entry
    - res: dictionary representing the entry
    """
    sections = line.split('\t')
    return {
      "word": sections[0].strip(),
      "valence": sections[1].strip(),
      "arousal": sections[2].strip(),
      "dominance": sections[3].strip()
    }

  def run(self):
    """
    Runner that processes all words in [self.lines]
    Writes to files by first letter
    """
    for line in self.lines:
      line = line.lower().strip()
      entry = self.process_line(line)
      self.write(entry, f"tmp/vad-{entry['word'][0]}.json", True)
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
        "valence": <valence>,
        "arousal": <arousal>,
        "dominance": <dominance>
      }
    }
    """
    for filename in directory:
      if filename.is_file():
        if filename.name.endswith('json') and filename.name.startswith("vad-"):
          with open('./tmp/'+filename.name, "r") as f:
            currentList = json.load(f)
            for entry in currentList:
              dataset[entry["word"]] = entry
          os.remove('./tmp/'+filename.name)
    with open(self.outfile, "w") as f:
      json.dump(dataset, f, indent=2, sort_keys=True)
  
if __name__ == "__main__":
  vad = VAD()
  vad.run()