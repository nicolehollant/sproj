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

## 9/30

Look at dates, and track down specifics for differences between datasets

-- compile their data for each difference

## 10/4

Gather excerpts, gather criticism to get the meaning, ask about meaning and altered meaning