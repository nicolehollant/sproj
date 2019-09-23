import json

senselevel = {}
wordlevel = {}

with open("wordlevel/out/wordlevel.json", "r") as f:
  wordlevel = json.load(f)
with open("senselevel/out/senselevel.json", "r") as f:
  senselevel = json.load(f)

def get_diff(arr1, arr2):
  if len(arr1) > len(arr2):
    return set(arr1).difference(set(arr2))
  return set(arr2).difference(set(arr1))

def same_entries(arr1, arr2):
  diff = get_diff(arr1, arr2)
  return len(diff) == 0, diff

numdiff = 0
differences = []
differences_by_number = {}
sumdiffs = 0
maxnumdiffs = 0
for word in senselevel.keys():
  senseassoc = senselevel[word]["associations"]
  wordassoc = wordlevel[word]["associations"]

  same, diffs = same_entries(senseassoc, wordassoc)
  if not same:
    numdiff +=1
    difference_count = len(diffs)
    sumdiffs += difference_count
    if difference_count == max(len(senseassoc), len(wordassoc)):
      differences_by_number["ALL"] = differences_by_number.get("ALL", 0) + 1
    else:
      differences_by_number[difference_count] = differences_by_number.get(difference_count, 0) + 1
    if difference_count > maxnumdiffs:
      maxnumdiffs = difference_count
    differences.append(diffs)
    print("\n", word)
    print("Sense Assoc:", senseassoc)
    print("Word Assoc:", wordassoc)
    print("Differences:", diffs)

  


print("\nTOTAL NUM DIFFERENT", numdiff)
print(f"\t{round(100 * numdiff/len(senselevel.keys()), 3)}% different")
print(f"\taverage difference count: {sumdiffs/len(differences)}")
print("Differences by number:")
for key, val in differences_by_number.items():
  print(key, val, round(val/numdiff, 3))