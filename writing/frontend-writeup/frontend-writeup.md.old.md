# Frontend

## In defense of the GUI

The client is often looked over within academic computer science, save for the developer as the end user. Running on the command line becomes a norm, and a repl becomes a coveted avenue in terms of UX so long as we are out of the realm of image processing. When we must focus on approachability, we tend to veer in a more interactive avenue: OOP with robots or using processing, intro web classes, games courses, Twine workshops in our orientation program, even languages like Scratch providing a gateway into programming. Then, after this introduction, we often lose the visual side of programming in favor of command-line-centered programming—the old bait and switch, as they say. Yet, visualization still rears its head every once in a while—the occasional GUI lab, rendering of search algorithms, and so on.

I, for one, am a lover of the visual interface. Why limit usability through negligence? Standard applications are comprised of sets of inputs and outputs, whether it's a social media platform, a file server, email client, even a calculator.

> Also Caleb is right apps are forms 👍🏻 most information systems are just friendly tuned UIs on top of a database. I think of something like Highrise as the prototypical web app.
> - Adam Wathan (@adamwathan), 5:58 PM · Oct 18, 2019

<!-- 
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">I would say GitHub is not the perfect example if only because most apps are honestly simpler, and don’t have complexity like doing all this crazy stuff on top of git servers.<br><br>Even like Dribbble is just forms when it comes to what makes it a real “app”.</p>&mdash; Adam Wathan (@adamwathan) <a href="https://twitter.com/adamwathan/status/1185314152425897985?ref_src=twsrc%5Etfw">October 18, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
-->

There's something remarkable about having a usable product, despite the associated challenge. There's also a certain gain in implementing what is client-facing in terms of access and security. If we are to implement something usable, and potentially public, there's more to security than a slap on the wrist—via grade reduction—for using all public variables; there could be tangible risks in being public facing. To use myself as an example, in just the past year I've pushed up my personal AWS keys (they were scraped and a few hundred dollars of EC2 instances were run up overnight), even this project was hacked (before adding admin credentials to my Mongo instance, my collections were all dropped and a ransom note was left as a new document requesting bitcoin to be sent in exchange for my data). The whole world of security changes when making something real, hence the heavy load of infrastructure in this project, and all to have a usable frontend. 

I love CLI tools. I had my i3wm and polybar, dotfiles-on-github phase. I had meme scripts, and some of them might even be funny to the right people (playing 90's hip-hop through "mpg123" and calling it "G-Unix" was my personal favorite). I cycled through terminal emulator after terminal emulator (urxvt is the best, of course); I went all in with vim as my editor. And once that chip on my shoulder grew stale (not like the T430's i7-3520M would ever be past its prime), I realized my mother would never quite appreciate what I was doing. The requisite motherly smile and nod is one thing, but she'd never show off my dotfiles to her friends, and thus we have embarked on our journey of making UIs.

<!-- This section title is what makes me happy -->
## Sap Aside / GSAP Inside

As per Adam Wathan's tweet, we'll more or less wrap our database operations, and our model as our UI. Our whole frontend is conceptually simple: we already have all the data, we just have to display it. Of course, some of this simplicity stems from foresight in the production of our API, but that's neither here nor there.

As with the rest of our project, we'll be going quite in-depth with our UI. That means no external component libraries, no pre-made templates, and, of course, no static site generators; if we are putting in the effort to make a UI, it should be ours, not BootStrap's. Our `package.json` has quite few dependencies, more or less `fontawesome` (icons), `gsap` (animation platform), `markdown-it` (markdown renderer), `tailwindcss` (utility-based css framework), and `vue` (our framework of choice). We aren't all that dependent on any of these dependencies, it wouldn't change too much to go an all-vanilla HTML/CSS/JS route, but these provide us with a bit of a break, and allow for some better performance.

### Configuration

There's not too much configuration to be done here as per the fairly minimal frontend and the niceties that Node has to offer. There are a few config files to edit to get tailwind integrated, and we have to deal with our old friend, webpack, for raw loaders for importing text files as strings. We set a `NODE_ENV` within our start scripts to be able to target different URI's for our API / model, and we have a rather simple router that maps from path to component file. This router just informs rendering, as did the Mux router in our Go API and the Flask router for our model, but, rather than giving `application/json`, we have our beautiful markup. 

## Creating our Component Library

some bit on sfc, js modules, lifecycle hooks, functional vs full-featured components 

### Abstracted renderers

some bit on more complex components that don't inform behavior, but rather display data

## Overview of Views

go into some detail with hitting endpoints, processing responses, translating to UI state

## Making things pretty

talk about css, you know quite a bit about it

or save it for comosus, whatever