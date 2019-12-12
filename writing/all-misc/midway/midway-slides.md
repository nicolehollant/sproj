<div class="midway-slide">

# Midway

</div>
<div class="midway-slide">

## Shifting Tone of a Body of Text

Cole Hollant

Stefan Mendéz-Diez, Bob McGrail, Kerri-Ann Norton






</div>
<div class="midway-slide">

## Intro / Refresher

- Natural language processing
  - Tone recognition: label input text
  - Tone alteration: change input text to align with a different category
- Plutchik's basic emotions
  - Joy, trust, fear, surprise, sadness, disgust, anger, anticipation

</div>
<div class="midway-slide">

## Super High Level Overview

- Host everything
- Make datasets
- Make models
- Bask in how well it works?







</div>
<div class="midway-slide">

## Hosting

And all the associated fun

</div>
<div class="midway-slide">

## Hosting Strategies

IaaS vs PaaS

<!-- 
  Talk about what IaaS and PaaS are
  - IaaS: renting server
  - PaaS: using environments
  
  We went with IaaS
-->

</div>
<div class="midway-slide">

## Our Choice

IaaS: Digital Ocean

<!-- 
  We just have a little ubuntu server somewhere (probably virginia or NY)
  - $5 a month for 1 core, 1gb ram, 1tb data transfer, 25gb storage
    - might have to scale up because we are real low on ram when building
  
  This means we have to do nearly everything ourselves
-->

</div>
<div class="midway-slide">

## Some records

- Domain from Google (colehollant.com)
- A whole lot of A records (for subdomains and ssh)
  - Also make sure to disable ssh for root!
- Point to a couple of DigitalOcean's name servers
<!-- 
  A (IPv4 address) Records: map the domain name of a host to the IP address of that host (name-to-address mapping).

  Name Server: The authoritative name server for the domain (holds the resource records).
-->

</div>
<div class="midway-slide">

## Git

Nothing too major for now, just beats scp for file transfer

*Might* move to GitHub orgs soon

</div>
<div class="midway-slide">

## Nginx

Our dear friend "Reverse Proxy"

- forward proxy: client-side
- reverse proxy: server-side
  - filter services

</div>
<div class="midway-slide">

## SSL/TLS

Secure Sockets Layer / Transport Layer Security

Save ourselves from http embarrassment
- just use certbot and add certs to server blocks
  - auto-rewrite insecure requests

</div>
<div class="midway-slide">

## Docker

VMs sans OS

Code neatly packaged with requirements, dynamic resource allocation

Each service needs a dockerfile
- walks through running the app (installing requirements, building, etc)
- multi-stage dockerfiles for small containers
  - why carry node runtimes if we don't need to

</div>
<div class="midway-slide">

## Docker Compose

My devops dream 😍

Yaml describing docker services
- specifies environment variables, port mappings, etc
- allows for some easy networking so my containers can chat
- absurdly easy to spin up and tear down

</div>
<div class="midway-slide">

## Mongo

Our NOSQL db!
- everything is JSON (or BSON, I guess...)
- we have to store things somehow
- security and abstraction with docker

<!-- 
  in an awkward place in the deck... 
  talk about getting hacked, how that shows pros of docker
  how it informed security

  mayyybe get into schema?
-->

</div>
<div class="midway-slide">

## Future Plans

- Set in stone for now
- Should make a cronjob for certbot
- Should set up webhooks
- *May want some custom email servers in the future*
- May want to move to Kubernetes 😎

</div>
<div class="midway-slide">

## Things Work 

Everything works now!

But, I'd hate to be satisfied

</div>
<div class="midway-slide">

## Cron Jobs

I'm positively tired of manually updating my SSL certs

</div>
<div class="midway-slide">

## Web Hooks

Web Hooks (from GitHub) would allow me to auto update on push

Alternatively: pipelines (either GitHub actions or moving to GitLab)

</div>
<div class="midway-slide">

## Email Servers

Email servers are iffy
- hard to set up
- can add consistency (UX 👍)
- no more reliance on SaaS

</div>
<div class="midway-slide">

## Kubernetes!!

Kubernetes is just *cool*
- again, hard to set up
- lots of scalability pros!
  - container orchestration
    - load balancing
    - auto scaling
    - rolling updates







</div>
<div class="midway-slide">

## Datasets

Everything comes from somewhere

</div>
<div class="midway-slide">

## Thesaurus

Web scraped from words.bighugelabs.com
- had all the data we wanted, in a format we could scrape
  - consistent layout, no robots.txt

Spider based on the unix words file

Write as we go, fix JSON after

</div>
<div class="midway-slide">

## Lexicons

From National Research Council Canada (NRC) / Saif M. Mohammad
- Built off of wordnet and emolex
- Utilized mechanical turk

Got Affect-Intensity, Color, Emotion, and VAD lexicons

TSV to JSON scripts

</div>
<div class="midway-slide">

## POSTing

Have "master JSON" locally

Just loop over entries and POST to our db

</div>
<div class="midway-slide">

## Future

- Google NGrams
  - Found scraper / api
- Twitter scraping for improved emotion lexicon







</div>
<div class="midway-slide">

## Our API

Go

</div>
<div class="midway-slide">

## Why

Interfacing with frontend sans JAM
- Need data from DB
- Can't interface directly

</div>
<div class="midway-slide">

## But... Why Go?

Experience
- Doing things in Python is quite easy (see model)
- Doing things in Go is quite hard
- When things are hard, we get a better understanding

</div>
<div class="midway-slide">

## Protocols and the Likes 🙃

- REST & CRUD
- HTTP
- TLS
- CORS

</div>
<div class="midway-slide">

## Main Process

- make db connection
- register endpoints
- apply middleware
- start server

</div>
<div class="midway-slide">

## Schema

- define schema per db collection
- structs with marshalling annotations

</div>
<div class="midway-slide">

## Utils

- provide nice wrapper functions 
  - ease of replication
  - ease of consistency
  - easy to manage
- wrap CRUD and common responses

</div>
<div class="midway-slide">

## Endpoints

Use those utils!

Pretty formulaic application of utility functions
- schema specific extensions
- room to refactor

</div>
<div class="midway-slide">

## Future API Plans

Hopefully nothing!

Maybe refactoring a bit

Maybe adding endpoints if we are changing datasets




</div>
<div class="midway-slide">

## Frontend

My happy place: Vue

</div>
<div class="midway-slide">

## Libraries

I'd never dream of using other component libraries

🙅‍♀️ BootStrap 🙅‍♀️

</div>
<div class="midway-slide">

## (post)CSS (My Favorite Thing on Earth)

*Bard's greatest fear*

Currently using Tailwind

Hopefully scrapping it for Comosus 🍍💝

</div>
<div class="midway-slide">

## Vue (My Second Favorite Thing on Earth?)

The Python of frameworks (but fast...)

</div>
<div class="midway-slide">

## Routing

A few pages:
- home: some landing page
- thesaurus: our thesaurus
- model: our model
- writing: our writing

Simple list of objects with path/name/sfc

</div>
<div class="midway-slide">

## Component Library

Components range in complexity
- navbar
- small UI components (slider, toggle, array renderers)
- more complex renderers (api results)

More should be functional, or maybe component factories

</div>
<div class="midway-slide">

## Views

The page layouts
- filled with components and other markup

Either standard HTML templates or render functions

</div>
<div class="midway-slide">

## The Actual JS

business logic and state logic
- fetching and processing data from api
- tracking UI state
- creating DOM elements / conditional rendering (directives)
- event emitting / handling

</div>
<div class="midway-slide">

## Future Frontend Plans

UX niceties
- suggested words
- themes
- better accessibility

Sweeping changes
- use Comosus 😎
- more functional components

Changing up data visualization

Adding more as we go





</div>
<div class="midway-slide">

## Model

the big "TODO"

</div>
<div class="midway-slide">

## Additional Service

The more the merrier!

</div>
<div class="midway-slide">

## Why Python?

&lt;img src="https://staples.com/easy-button.mp4"&gt;

</div>
<div class="midway-slide">

## How does it work?

- receive requests from frontend
  - parse them, pass to appropriate endpoints, etc
  - flask is a cakewalk
- text preprocessing (dealing with punctuation, etc)

</div>
<div class="midway-slide">

## Control Model

Make a whole bunch of calls
- each word gets a random synonym
- log things that don't exist

Options:
- replacement probability
- ignore stop words

</div>
<div class="midway-slide">

## Future Plans

Make main LDA model

Perhaps look into NN if we must

</div>
<div class="midway-slide">

## LDA

- generative statistical topic model
  - document &rarr; set of topics
- Bayesian inference for topic mixture
- Soft clustering
  - fuzzy membership
  - topic reduction

</div>
<div class="midway-slide">

## LDA thoughts

Just for analysis 

Seed with words by association
- maybe weight by strength

Change words until it realigns
- criteria for changing





</div>
<div class="midway-slide">

## Odds and Ends

Related bits

</div>
<div class="midway-slide">

## Metrics

The boring part

</div>
<div class="midway-slide">

## User Testing

IRB 😴

Do some sort of user testing

Do some analysis on it

</div>
<div class="midway-slide">

## Writing Conversion

I'm too lazy for Latex / don't like it

</div>
<div class="midway-slide">

## The End

Here are links if anyone is interested
- Frontend: [sproj.colehollant.com](https://sproj.colehollant.com)
- Backend: [sproj.api.colehollant.com](https://sproj.api.colehollant.com/thesaurus/api/v1/words/cool)
- Version control: [my github](https://github.com/colehollant/sproj)

</div>