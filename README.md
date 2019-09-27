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
     * Consider kmc !!!! gotta pretend i know about linalg and separatrices or whatnot
   4. Maybe just dont do NNs:
     * look at LDAs and seeded LDAs
     * I don't like NNs :'-(

## Frontend todo:
   * interface on site for model
   * fuzzy search for words (maybe publish some edit distance thing on npm)
   * break up frontend dockerfile so that I can have a dev image (that just runs `yarn serve` and attaches my dirs)
     * read [this](https://hackernoon.com/a-better-way-to-develop-node-js-with-docker-cd29d3a0093)
   * would also love to break up more things into components and do a design doc
   * gotta use tailwind better

## Backend todo:
   * deal with go modules (maybe provide the actual git path?)
   * write better / more reusable code
   * post all the things in `db` to separate collections
   * maybe change the admin-words endpoints to take in a collection name?
   * endpoint to get all available data

## Writing todo:
   * write up frontend/backend for thesaurus
   * write about the stuff in `db`