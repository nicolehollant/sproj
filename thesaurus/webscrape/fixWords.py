#/bin/python3

'''
Tiny script to remove entries with 
apostrophes from [wordsWithApostrophes]
'''
with open('wordsWithApostrophes', 'r') as infile:
    with open('words', 'w') as outfile:
        for word in infile.readlines():
            # ignore words with apostrophes
            if word.find("'") == -1:
                outfile.write(word)