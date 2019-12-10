"""
Helper Script to make markdown tables from .bib files!
- For the ease of citation!
- USAGE:
  python bibToMD.py <INPUTFILE.bib> [-o <OUTPUTFILE.md>]
"""

import sys 

def map_citations(fname):
  citations = []
  current = {}
  with open(fname, 'r') as f:
    for line in f.readlines():
      line = line.strip()
      lowerline = line.lower()
      line = line.replace("|", "\\|")
      if lowerline.startswith('@') and line.find('{') > 0:
        current['cite'] = line[line.find('{') + 1: -1]
      if lowerline.startswith('howpublished') and line.find('{') > 0:
        current['published'] = line[line.find('{') + 1:].replace('\\url{', '').replace('}},', '')
      if lowerline.startswith('title') and line.find('{') > 0:
        current['title'] = line[line.find('{') + 1:].replace('},', '')
      if lowerline == '}':
        citations.append(current)
        current = {}
  return citations

def write_md_table(citations, outfile=None):
  table = []
  header = "| Cite | Tite | Reference |\n"
  spacer = "|------|------|-----------|\n"
  table.append(header)
  table.append(spacer)
  for citation in citations:
    cite = citation.get('cite', '')
    title = citation.get('title', '')
    published = citation.get('published', '')
    table.append(f"| {cite} | {title} | {published} |\n")
  if not outfile:
    for line in table:
      print(line)
  else:
    with open(outfile, 'w') as f:
      f.writelines(table)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Please pass a path to a bib file")
    quit(1)
  elif "-o" in sys.argv:
    try:
      outfile = sys.argv[sys.argv.index("-o") + 1]
      write_md_table(map_citations(sys.argv[1]), outfile=outfile)
    except:
      print("No output file specified, but one was requested")
      quit(1)
  else:
    write_md_table(map_citations(sys.argv[1]))