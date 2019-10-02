Maybe can use [this](https://www.allmusic.com/advanced-search) to get lyrics with given moods?

peep more dns stuff: 
* https://www.digitalocean.com/community/tutorials/an-introduction-to-dns-terminology-components-and-concepts
* https://www.digitalocean.com/docs/networking/dns/


Nginx stuff: 

`sudo vim /etc/nginx/sites-available/colehollant.com`

`sudo ln /etc/nginx/sites-available/sproj.colehollant.com /etc/nginx/sites-enabled/sproj.colehollant.com`

(def need sysctl)
* GOOD ONE: https://dev.to/on_stash/configure-nginx-to-host-multiple-subdomains-2g0b

* https://serverfault.com/questions/538803/nginx-reverse-ssl-proxy-with-multiple-subdomains
* https://stackoverflow.com/questions/23649444/redirect-subdomain-to-port-nginx-flask
* https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-as-a-web-server-and-reverse-proxy-for-apache-on-one-ubuntu-18-04-server


## Crowdsourcing a Word-Emotion Association Lexicon

[Cited by many](https://scholar.google.com/scholar?um=1&ie=UTF-8&lr&cites=5645606000352711478)

### Abstract

Crowdsourcing as is "quick, inexpensive"
Word choice question (def?) discourages malicious data entry, identify lack of word knowledge.
Asking for association leads to higher *inter-annotator agreement* than asking for emotion evokation

### Intro - 6

Introduces sentiment analysis (determining the opinions and private states of the speaker towards a target identity).
Lately, *positive/negative polarity* (semantic orientation/valence) is used to determine favorable/unfavorable opinions towards something. Not that much regarding emotion

Their lexicon provides term-emotion association (how strongly the term is associated with the emotion)
They gave annotators examples of words associated with different emotions, and they relied on intuition to mark emotions (did not give defs)

Emotion dependent on context

Currently WordNet Affect Lexicon, General Inquirer, Affective Norms for English Words exist

They used Amazon's Mechanical Turk, focused on [joy, sadness, anger, fear, trust, disgust, surprise, anticipation] (from phutchik's wheel of emotions), unigrams and bigrams. Used the "Macquarie Thesaurus"

Took terms occuring frequently in Google's n-gram corpus. Took 200 most frequent unigrams and bigrams for each pos (n, v, adv, adj), ignoring those that occurred in multiple POS

### Issues

QA/QC, educational background, direction adherance, money, english skills

### Approach

Prune responses with bad answers, generated word choice problems automaticaly with the Macquarie Thesaurus (pg 10 sample HIT)