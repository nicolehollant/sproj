import sys
from .train import train
from .score import eval_text
from pprint import pprint

def print_help():
  print("To run:")
  print("python3 -m lda")
  print("\nOptions:")
  print("\t-t | --train\t\ttrains model")
  print("\t-e | --eval\t\tscores the passed arguments as input")
  print("\t-h | --help\t\tprints this help message")

if __name__ == "__main__":
  if len(sys.argv) < 3 and '--train' in sys.argv or '-t' in sys.argv:
    train()
  elif len(sys.argv) < 3 and '--help' in sys.argv or '-h' in sys.argv:
    print_help()
  elif '--eval' in sys.argv or '-e' in sys.argv:
    if '--eval' in sys.argv: sys.argv.remove('--eval')
    if '-e' in sys.argv: sys.argv.remove('-e')
    pprint(eval_text(' '.join(sys.argv[1:])))
  else:
    print_help()