import json
import os

class Colour():
  """
  Manipulate the "NRC-Colour-Lexicon" dataset for our use

  FILE FORMAT (from their readme):
    Each line has the following format:
    <TargetWord>--<sense><tab>Colour=<colour><tab>VotesForThisColour=<VotesForThisColour><tab>TotalVotesCast=<TotalVotesCast>

    <TargetWord> is a word for which the annotators provided colour associations;

    <sense> is one or more comma-separated words that indicate the sense of the target word for which the annotations are provided;

    <colour> is the colour most associated with the target word. It is one of eleven colours---white, black, red, green, yellow, blue, brown, pink, purple, orange, grey. If each of the annotators suggested a different colour association for the target word, then <colour> is set to None.

    <VotesForThisColour> is the number of annotators who chose <colour> for the target word. It is set to None if <colour> is None.

    <TotalVotesCast> is the total number of annotators who gave colour associations for the target word.


  EX:
    aaaaaaah	0.479	0.606	0.291
  """

  def __init__(self):
    path = "../../resources/NRC-Sentiment-Emotion-Lexicons/NRC-Colour-Lexicon-v0.92/NRC-color-lexicon-senselevel-v0.92.txt"
    self.lines = open(path, 'r').readlines()
    self.outfile = "out/colour.json"
    self.dataset = {}

  def process_line(self, line):
    """
    process a line
    
    @params: line -- a line of text as per the file format:
    - <TargetWord>--<sense><tab>Colour=<colour><tab>VotesForThisColour=<VotesForThisColour><tab>TotalVotesCast=<TotalVotesCast>
    Sections:
    - <TargetWord>--<sense>
      Colour=<colour>
      VotesForThisColour=<VotesForThisColour>
      TotalVotesCast=<TotalVotesCast>
    @returns: 
    - complete: boolean indicating finished state of entry
    - res: dictionary representing the entry
    """
    sections = line.split('\t')
    wordsection = sections[0].split('--')
    word = wordsection[0].strip()
    sense = wordsection[1].strip()
    color = sections[1].split('=')[1].strip()
    votes = sections[2].split('=')[1].strip()
    totalvotes = sections[3].split('=')[1].strip()
    return {
      "word": word,
      "sense": sense,
      "color": color,
      "votes": votes,
      "totalvotes": totalvotes
    }

  def run(self):
    """
    Runner that processes all words in [self.lines]
    Writes to files by first letter
    """
    for line in self.lines:
      line = line.lower().strip()
      entry = self.process_line(line)
      self.write(entry, f"tmp/colour-{entry['word'][0]}.json", True)
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
        if filename.name.endswith('json') and filename.name.startswith("colour-"):
          with open('./tmp/'+filename.name, "r") as f:
            currentList = json.load(f)
            for entry in currentList:
              dataset[entry["word"]] = entry
          os.remove('./tmp/'+filename.name)
    with open(self.outfile, "w") as f:
      json.dump(dataset, f, indent=2, sort_keys=True)
  
if __name__ == "__main__":
  Colour = Colour()
  Colour.run()