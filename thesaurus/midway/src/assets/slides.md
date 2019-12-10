# Midway

## Shifting Tone of a Body of Text

Cole Hollant

Stefan Mendéz-Diez, Bob McGrail, Kerri-Ann Norton



============================================================



## Intro / Refresher

- Natural language processing
  - Tone recognition: label input text
  - Tone alteration: change input text to align with a different category
- Plutchik's basic emotions
  - Joy, trust, fear, surprise, sadness, disgust, anger, anticipation

## Super High Level Overview

- Host everything
- Make datasets
- Make models
- Bask in how well it works?




============================================================



## Hosting

And all the associated fun

## Hosting Strategies

IaaS vs PaaS

<!-- 
  Talk about what IaaS and PaaS are
  - IaaS: renting server
  - PaaS: using environments
  
  We went with IaaS
-->

## Our Choice

IaaS: Digital Ocean

<!-- 
  We just have a little ubuntu server somewhere (probably virginia or NY)
  - $5 a month for 1 core, 1gb ram, 1tb data transfer, 25gb storage
    - might have to scale up because we are real low on ram when building
  
  This means we have to do nearly everything ourselves
-->

## Some records

- Domain from Google (colehollant.com)
- A whole lot of A records (for subdomains and ssh)
- Point to a couple of DigitalOcean's name servers
<!-- 
  A (IPv4 address) Records: map the domain name of a host to the IP address of that host (name-to-address mapping).

  Name Server: The authoritative name server for the domain (holds the resource records).
-->



## Future Plans

- Set in stone for now
- *May want some custom email servers in the future*
- May want to move to Kubernetes 😎

## Things Work 

Everything works now!

But, I'd hate to be satisfied


<!-- 
  I want a custom email so that I can do forms in a cool way
  I want kubernetes cause it's so cool!!!!
  - I want to have auto-scaling
  - I want to have

-->