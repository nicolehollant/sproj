# Prospectus Talk

You will give a short five minute presentation to the computer science community in the seventh week of the first term. 
You should describe the problem your senior project is addressing, 
explain why it is interesting, 
and include an evaluation plan.

Please share with me a google slides presentation by October 30th.

<!-- 
  My moves:
  - Title
  - Abstract
  - High level plans
  - Current progress
  - (maybe next steps?)
-->

## Slide 1 (Title)

Shifting tone of a body of text

Cole Hollant

<!-- 
  Just introduce yourself lol
-->

## Slide 2 (Abstract)

- Natural language processing
  - Tone recognition: label input text
  - Tone alteration: change input text to align with a different category
- Plutchik's basic emotions
  - Joy, trust, fear, surprise, sadness, disgust, anger, anticipation

<!-- 
  We will be looking into altering the tone of a body of text based off of Robert Plutchik's basic emotions while preserving the original meaning. This project encompasses building probabilistic models in the realm of natural language processing (nlp), full-stack web development, dataset creation and application, along with proofs of algorithmic runtimes. We will build our models off of latent Dirichlet allocation—a grouping model common in nlp—and may explore neural networks as a means of emotion recognition. This will also involve user testing as a means of measuring the effectiveness of our models as well as guiding the development cycles.
-->

## Slide 3 (High Level Plans)

- Build out datasets / lexicons
  - Sourced vs created
    - NRC Emotion / Affect lexicons
      - Unigram limitations
    - Twitter scraper
    - Scraped thesaurus
- Make different models
  - Arbitrary replacement (control)
  - LDAs
  - Neural nets?
    - Potential n-gram benefits
- User testing

<!-- 
  Talk mostly about ldas
  Talk about how I built / restructured the datasets
  Talk about different models (arbitrary as control, others as more involved actual things)
  Talk about user testing
  - Maybe drop a form on my landing page
-->

## Slide 4 (LDAs)

Latent Dirichlet Allocation
- generative statistical topic model
  - document &rarr; set of topics
- Bayesian inference for topic mixture
- Soft clustering <!-- Contrast to k-means which is only allows one group -->
  - fuzzy membership
  - topic reduction

## Slide 4 (Current Progress)

- Thesaurus
- Lexicons
- Website
  - Frontend
  - API
  - Server setup, etc

<!--
  Maybeeeee talk about process on each of these
-->

## Slide 5 (Next Steps)

- More server configuration
- Build LDA model
- Alter data visualization

<!--
  Just gloss over this stuff
-->

## Slide 6 (Thank you!)

Here are links if anyone is interested
- Frontend: [sproj.colehollant.com](https://sproj.colehollant.com)
- Backend: [sproj.api.colehollant.com](https://sproj.api.colehollant.com/thesaurus/api/v1/words/cool)
- Version control: [my github](https://github.com/colehollant/sproj)

<!--
  We love an outro plug!
-->