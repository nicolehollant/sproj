# Future Work

Given both the state of the world at the end of this academic year and the scope of this project, there is material left undone. This section serves to address that, both in the sense of acknowledgment and with ideas for implementation if applicable.

- Should have an LDA replacement model
- Should be able to train an LDA from the site (to control hyperparameters)
- Should maintain db connection from model api
- Should determine a better way to deliver topic scores (not just importing json). This would depend on whether or not there is an LDA training component for whether or not it would be something that is per session or added to the DB
- Better interaction from the frontend (auto-analysis for what words are affecting output, ability to alter words manually-from dropdown of synonyms or manual entry-that is reactive)
- Migrate to graphql (more appropriate for something like this)
- Corpus creation tool (allow for overriding base synonyms/antonyms/scores adding new words, etc on a per-user basis -- would necessitate auth and larger db)
- Extend light/dark mode for some smaller pieces (docs, info popover, etc) (maybe also user-defined themes?)
- More info popovers throughout the site!
- Perhaps abstract the doc-components to a doc-gen tool so other ppl can use it
- Use a proper server for the models lol (although, prob would have unification of apis if moving to gql)
- UI playground and more complete component library
- Some other UI niceties (integrate color corpus!!) and things like fuzzy search
- Should auto-score output from replacement models, or at least give routerlinks in the results section to go to the scoring models (prob query string stuff)