# sproj
Senior Project BABYYYYY

## Stuff that's live:
Frontend - http://sproj.colehollant.com
Backend - http://sproj.api.colehollant.com


# TODO:

* move 2 gitlab ( LOL ) ... unless we wait 4 github ci
* ~~DNS stuff :-(~~
## Project Model Stages (maybe?)
  1. Random replacement:
     * ~~Feed in a body of text, set some probability of word replacement, switch a word~~
  2. Bayesian replacement (LDA model):
     * Gather >= 2 categories, gather some probabilities of words belonging to a category (we will ignore words not in my thesaurus, but maybe write them to a file?), calculate probs of word being used given each category, replace with word if prob of belonging to the other category is greater (or lesser)
  3. Neural Network replacement:
     * Consider kmc !!!! gotta pretend i care about linalg and separatrices or whatever
   4. Maybe just dont do NNs:
     * look at LDAs and seeded LDAs

## Frontend todo:
   * interface on site for model
   * fuzzy search for words (maybe publish some edit distance thing on npm)
   * break up frontend dockerfile so that I can have a dev image (that just runs `yarn serve` and attaches my dirs)
     * read [this](https://hackernoon.com/a-better-way-to-develop-node-js-with-docker-cd29d3a0093)
   * would also love to break up more things into components and do a design doc
   * gotta use tailwind better



# Meetings

## 9/9

- read 'Crowdsourcing a WordEmotion Association Lexicon', write summary, maybe look at recreating results 
	- look at articles that cite it
- look more into LDAs and how we might be able to use them
- think about compliance w/ gathering data :(


## 9/16

Talk to keith about digital humanities ppl that could help, also maybe pysch ppl

think about probability of phrase being said (comparing ngram probabilities?)
- https://books.google.com/ngrams

going to need surveys (checking results), need to see what I need to be compliant

- start moving lexicon to mongo
- list how the studies classify words
- new collections per lexicon

```yaml
lexicon:
- word:
   - associations:
      -  

```



```json
{
   "word": "coffee",
   "associations": [ // prob go with this
      "happy", "trust"
   ],
   "associations": {
      "happy": 1,
      "trust": 1,
      "anger": 0,
      ...
   }
}

```

## 9/23

- Redo sense-level (there are multiple entries in the TSV, fix your JSON to actually get that)
  - probably can keep most of the code, but maybe switch to use arrays?
    - could potentially check existence of key at write time and add if exists