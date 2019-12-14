# Lexicons

<!-- 

Questions:
- what exatly is word-sense? is it [this](https://en.wikipedia.org/wiki/Word-sense_disambiguation)
  - Answer: from wikipedia "Words are in two sets: a large set with multiple meanings (word senses) and a small set with only one meaning (word sense)"

-->

## National Research Council Canada (NRC) Emotion Lexicon

### IMPORTANT NOTE: remember to cite as per Terms of Use in their readme

This is the lexicon that we are most interested in as it is most directly related to our project. There are two forms of this lexicon: the "word-sense" lexicon is the original annotated at the word-sense level and the "word" lexicon is a baked version which condenses all word-senses for a word.

We've made some mistakes in the past, so we want to check our restructured data; if we know that the "word-level" form was created by taking the union of the affect associations of the "sense-level" form, we can create our own version of the "word-level" and compare the two versions. As there's little sense in keeping our own version around, we may check it algorithmically.

### Methodology

Saif M. Mohommad and Peter D. Tourney compiled this lexicon with crowdsourcing through Amazon's Mechanical Turk (an online crowdsourcing platform); they chose crowdsourcing as it is quick and inexpensive (costing them $2100 for the Turkers). As a deterrent of bad responses, they included a filtering question in each survey that asked for the best synonym for the given word, allowing them to identify either lack of word knowledge or probabilitically filtering random responders. They selected joy, sadness, anger, fear, trust, disgust, surprise, and anticipation as per Robert Plutchik's wheel of basic emotions, as well as drawing from the present emotion lexicons WordNet Affect Lexicon, General Inquirer, and Affective Norms for English Words and both the Maquarie Thesaurus and Google's N-Gram corpus. They generated questions with the Macquarie Thesaurus with the aforementioned filtering-question followed by questions asking for alignment with the various emotions. They also included polarity (positive vs negative valence) in the lexicon, giving us 10 categories to work with.

<!-- Maybe delve into Plutchik? -->

## Our Representation

We wanted to preserve their data, but bring it into our database (MongoDB). This transfer was relatively painless, as their lexicon was in consistent TSV. We borrowed a decent amount of JSON utilities and structure from our thesaurus-scraper, writing to files by first letter as we go; all that changes is the shift from making http requests and parsing HTML to loading a local file and parsing TSV. We did this for both the "word-level" and the "sense-level" forms resulting in the following schema:

### Word Level
```json
{
  "<word>": {
    "associations": [
      "<list",
      "<of>",
      "<associations>",
    ],
    "word": "<word>"
  },
  ...
}
```

### Sense Level

```json
{
  "<word>": [
    {
      "sense": [
        "<list",
        "<of>",
        "<synonyms>",
      ],
      "associations": [
        "<list",
        "<of>",
        "<associations>",
      ],
      "word": "<word>"
    },
    ...
  ],
  ...
}
```

### Word-Sense Level

Note that the sense-level scheme consists of arrays whose entries resemble the word-level scheme along with a field representing the word-sense; this is because the word-level representation of a word is created from the union of the sense-level entries for that word.

> The original lexicon has annotations at word-sense level. Each word-sense pair was annotated by at least three annotators (most are annotated by at least five). 
> The word-level lexicon was created by taking the union of emotions associated with all the senses of a word. 
> — Saif M. Mohammad and Peter D. Turney (from NRC-Emotion-Lexicon-v0.92/readme.txt)

Each entry from these forms can then be easily POST-ed to our API and can be accessible!

### Other lexicons

The other lexicons that we are using are the National Research Council Canada (NRC) Colour Lexicon, Affect-Intensity Lexicon, and VAD Lexicon. These three followed largely from the first. They shared similar formats, and we only had to change how we parsed them. These lexicons were all one-entry-per-line, so we were able to skip our finished-entry checking, and otherwise the differences were solely in the `process_line` which had to be catered to each lexicon. As they are also single-form, we skipped difference checking for all of them.

### Potential Downfalls

As per the construction of these lexicons, there are some legitamate cons. The most jarring is in the sense of everything being a unigram. With a limited understanding of language, one notices that a word's meaning depends on surrounding words. As these lexicons are manufactured without context, we lose this crucial aspect of how words relate to and affect one another. For the first model, we will not do anything about this at the dataset level; there is, however, some room to account for this in the model. Google has an NGrams API which holds data regarding the probability of a sequence of words being used within the collection of Google books in a specified time period. This may allow for us to have a certain level of control where we may take whether a sequence of words is likely to occur into consideration.

In the long term, as this is not an elegant solution, we may consider altering our dataset. For this we would likely go through with scraping Twitter; this would provide us with a large amount of data that we can apply certain criteria to. We can decide on rules for when a tweet is classified as belonging to a given emotion category: perhaps based off of hashtags, keywords, or emojis. This then would allow us to command control over our dataset, where we can take any data we see fit—most notably, n-grams.