"""
Silly little script to assemble one file out of all the scattered bits
"""

def compile_writing(outfile="all-writing.md"):
  res = []
  paths = [
    'thesaurus-writeup/thesaurus-writeup.md',
    'server-writeup/server-writeup.md',
    'lexicons-writeup/lexicons.md',
    'backend-writeup/backend-writeup.md',
    'frontend-writeup/frontend-writeup.md',
  ]
  for path in paths:
    res+=open(path, 'r').readlines()
    res+=["\n", "\n", "\n"]
  with open(outfile, "w") as f:
    f.writelines([line for line in res])


if __name__ == "__main__":
  compile_writing()


