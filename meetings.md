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

## 10/24

DO WRITING!!!!
Prepare prospectus talk for comp sci
- maybe add beginning random model to site before the talk? (depends on how easy that will be)

Display each association (including from any synonym):
- under each, give all synonyms

(get senselevel associations for each synonym, keeping track of their associations, adding to them)
Slides to stefan for monday

Wordlevel from senselevel (add "all" field)

Create local master list (query each endpoint)

Send an email to the authors asking about word-level vs sense-level?

## 10/28

Prepare for talk
Send Stefan 2+ pages by sunday night

- bib stuff!!!

- lexicons
- api

- design (for future)

# 11/1

- wrap in flask
- write rest of endpoints
- steal stuff from wordnet!
  - grab emotion association by tweets?
  - maaaybe look into facebook?

Peep "Speech and Language Processing (3rd edition)"

Ask bob what we need for IRB

# 11/11

- To the control model add:
  - [ ] Sentiment score
  - [ ] Frequency of use (unigram level)
    - Think about adding unigram frequency collection
      - Consider frequency by time period for n intervals

- [X] Add and proxy subdomain for model
- [ ] Add logging for each word and its wordlevel / affect intensity
- [ ] Consider compound sentiment
- [ ] Add all lexicons (and wordlevel) to frontend thesaurus page

Could potentially do a subproject to get started with LDAs:
Im thinking we could make a playlist generator. Not sure how much we can get from the spotify api, but if we can get all songs in a playlist, then we can scrape lyrics and try and build subset playlists with similar topic spreads?

Write LDAs first!!
Comment code over winter break

Midways: (Stefan, Kerri, Matt)
schedule for soon after winter break (late january?)
- Ask Sven to come to midway!!
- give a presentation on what I've done and what I'm planning to do 20-30 minute presentation
- by last day of semester submit 10 pages

IRB:
ask before and after
- reading comprehension and emotion!
- maybe passages from SAT prep for multiple choice
- how much did it change, in what way?
- separate out passages?
- SAT prep could be good!!

Documentation:
- module level descriptions in appendix or main writing?
- no docs in appendix

Email Justin Dainerbest ? about irb (also about stats)

Link to code in intro

Do multiple links per bib entry for stuff like MDN