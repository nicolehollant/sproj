import json
import os

class SenseLevel():
  """
  Manipulate the "NRC-Emotion-Lexicon-Senselevel" dataset for our use

  FILE FORMAT (from their readme):
    Annotations at WORD-SENSE LEVEL (file: NRC-Emotion-Lexicon-Senselevel-v0.92.txt)

    Each line has the following format:
    <term>--<NearSynonyms><tab><AffectCategory><tab><AssociationFlag>

    <term> is a word for which emotion associations are provided;

    <NearSynonyms> is a set of one to three comma-separated words that indicate the sense of the <term>. The affect annotations are for this sense of the term.

    <AffectCategory> is one of eight emotions (anger, fear, anticipation, trust, surprise, sadness, joy, or disgust) or one of two polarities (negative or positive);

    <AssociationFlag> has one of two possible values: 0 or 1. 0 indicates that the target word has no association with affect category, whereas 1 indicates an association.
  
  EX:
    gut--opening, fistula, tubule	fear	0
  """

  def __init__(self):
    path = "../../../resources//NRC-Sentiment-Emotion-Lexicons/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Senselevel-v0.92.txt" # NRC-Emotion-Lexicon-Wordlevel-v0.92.txt
    self.lines = open(path, 'r').readlines()
    self.outfile = "out/senselevel.json"
    self.dataset = {}
    self.currententry = {}
    self.currententry["associations"] = []

  def process_line(self, line):
    """
    process a line, adding current information to [currentword]
    - as this document has 10 lines per word, 
      we will check for the last of the 10 to return the completed entry
    
    @params: line -- a line of text as per the file format:
    - <term>--<NearSynonyms><tab><AffectCategory><tab><AssociationFlag>
    @returns: 
    - complete: boolean indicating finished state of entry
    - res: dictionary representing the entry
    """
    res = {}
    sections = line.split('\t')
    wordsect = sections[0]
    affect = sections[1].strip()
    association = sections[2].strip()
    if affect == "anticip":
      affect = "anticipation"

    word = wordsect.split("--")[0]

    self.currententry["word"] = word.strip()
    self.currententry["sense"] = [x.strip() for x in wordsect.split("--")[1].split(",")]
    if int(association) == 1:
      self.currententry["associations"].append(affect)

    complete = affect == "joy" # words come in 10s
    if complete:
      res = self.currententry.copy()
      self.currententry = {}
      self.currententry["associations"] = []

    return complete, res

  def run(self):
    """
    Runner that scrapes all words in [self.words]
    Writes to files by first letter
    """
    for line in self.lines:
      line = line.lower().strip()
      complete, entry = self.process_line(line)
      if complete:
        self.write(entry, f"tmp/senselevel-{entry['word'][0]}.json", True)
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
      "WORD": {
        "associations": [],
        "sense": [],
        "word": "WORD"
        ...
      }
    }
    """
    for filename in directory:
      if filename.is_file():
        if filename.name.endswith('json') and filename.name.startswith("senselevel-"):
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
  senselevel = SenseLevel()
  senselevel.run()