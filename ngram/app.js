const ngram = require('./ngram')
ngram.fetchNgram(['green', 'eggs']).then(results => console.log(results))