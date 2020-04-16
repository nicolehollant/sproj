import json
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import models

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
stopwords = ['ve', 'won', 'more', 'needn', "doesn't", 'most', 'each', 'down', 'should', "weren't", 'yourself', "didn't", 'on', 'below', 'whom', 'herself', 'your', "you'd", 'hers', 'you', 'about', 'because', 'up', 'me', 'can', 'out', "hasn't", 'him', 'again', 'is', 'same', 'were', 'a', "wasn't", 'd', "haven't", 'them', 'very', 'i', 'such', 'mightn', 'until', "mustn't", 'haven', 'off', 'here', 'it', 'isn', "won't", 'over', "that'll", 'the', "hadn't", 'wouldn', 'yourselves', 'was', 'we', 'both', 'doesn', 'been', 'when', "wouldn't", 'only', 'aren', 'has', 'why', 'do', 'weren', 'at', 't', 'from', 'how', 's', 'these', 'for', 'be', 'through', 'ourselves', 'to', 'where', 'of', "you're", 'in', 'he', "aren't", "shouldn't", "you'll", 'nor', 'didn', 'above', 'couldn', 'himself', 'than', 'hasn', 'they', 'so', 'm', 'but', 'other', "couldn't", 'll', 'its', 'then', 'there', 'some', 'too', 'shan', 'no', "she's", 'wasn', 're', 'hadn', 'being', 'what', 'this', 'are', 'our', 'myself', 'she', 'and', "isn't", 'does', 'that', 'while', 'own', 'having', 'against', 'had', 'by', 'their', 'my', 'did', 'shouldn', 'during', 'ma', 'now', 'or', 'into', 'few', 'themselves', 'once', "don't", 'her', 'any', 'will', 'ours', 'further', 'his', 'with', "shan't", "should've", 'just', 'after', "you've", 'yours', 'between', 'before', 'itself', 'theirs', 'ain', 'those', 'am', 'not', 'all', 'o', "mightn't", 'which', "it's", "needn't", 'who', 'under', 'y', 'mustn', 'if', 'have', 'an', 'doing', 'as', 'don']
# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
all_scores = json.load(open('lda/stems-scores.json', 'r'))
ldamodel = models.ldamodel.LdaModel.load("lda/ldamodel")
dictionary = ldamodel.id2word

def base_result():
  return { 'sadness': 0.0, 'joy': 0.0, 'fear': 0.0, 'anger': 0.0 }

def normalize_topic(topic_probabilities):
  res = {}
  total = sum(topic_probabilities)
  for i, entry in enumerate(topic_probabilities):
    res[dictionary[i]] = entry / total
  return res

def normalize_topic_keywords(topic_probabilities):
  res = {}
  total = sum(map(lambda a: a[1], topic_probabilities))
  for entry in topic_probabilities:
    res[entry[0]] = entry[1] / total
  return res

def score_keywords(keywords, keyword_coefs):
  res = base_result()
  for keyword in keywords:
    score = all_scores.get(keyword, {}).get('score', {})
    res['sadness'] += score.get('sadness', 0.0) * keyword_coefs.get(keyword, 1.0)
    res['joy'] += score.get('joy', 0.0) * keyword_coefs.get(keyword, 1.0)
    res['fear'] += score.get('fear', 0.0) * keyword_coefs.get(keyword, 1.0)
    res['anger'] += score.get('anger', 0.0) * keyword_coefs.get(keyword, 1.0)
  return res

def score_keywords_given_topic(keywords, probs):
  keyword_coefs = normalize_topic(probs)
  return score_keywords(keywords, keyword_coefs)

def score_keywords_given_keywords(keywords, probs):
  keyword_coefs = normalize_topic_keywords(probs)
  return score_keywords(keywords, keyword_coefs)

def score_input(keywords, probs):
  keyword_coefs = normalize_topic(probs)
  return score_keywords(keywords, keyword_coefs)

def score_topic(probs):
  keyword_coefs = normalize_topic(probs)
  return score_keywords([dictionary[i] for i in range(len(probs))], keyword_coefs)

def scale_scores(probability, scores): 
  res = {
    'sadness': probability * scores['sadness'],
    'joy': probability * scores['joy'],
    'fear': probability * scores['fear'],
    'anger': probability * scores['anger'],
  }
  return res

def add_scores(scores, current): 
  res = {
    'sadness': current['sadness'] + scores['sadness'],
    'joy': current['joy'] + scores['joy'],
    'fear': current['fear'] + scores['fear'],
    'anger': current['anger'] + scores['anger'],
  }
  return res
  
'''
So, the idea is that we seed the model with 4 documents (one for each emotion that we care about)
Then, from there, we let it figure out its own topic mixture. This is a some linear combination of word_stems.
  i.e.: topic 96 is: (96, '0.002*"depress" + 0.002*"devast" + 0.002*"pain" + 0.002*"reject" + 0.001*"disapprov" + 0.001*"regret" + 0.001*"banish" + 0.001*"abandon" + 0.001*"poison" + 0.001*"murder"')
then we would want to grab a score from that.
- define scores for each topic
  - go through all words in topic get frequency of affects by topic
  - maybe targeting keywords in replacement?
    - maybe only score keywords?
- consider running through old model and multiplying by that scalar?
- also consider giving the inverting the topic keywords (restem?)
  - might actually be necessary to do this to get score!!!
  - think I'm going to have to add a whole bunch to both lexicons
    Kinda like this
    - wordstem: {
      words: [word1, word2, ...],
      affect_list: [...],
      sense_list: [...]
    },
    - wordstem: {
      words: [word1, word2, ...],
      angry: 123,
      sad: 134,
      joy: 48
    }
'''

def get_doc_topics(lda, bow):
  gamma, _ = lda.inference([bow])
  topic_dist = gamma[0] / sum(gamma[0])  # normalize distribution
  return [(topicid, topicvalue) for topicid, topicvalue in enumerate(topic_dist)]

def eval_text(test, num_keywords=20, threshold=0.01):
  res = {}
  test_tokenized = tokenizer.tokenize(test.lower())
  test_stopped = [i for i in test_tokenized if not i in stopwords]
  test_stemmed = [p_stemmer.stem(i) for i in test_stopped]
  res['input_stemmed'] = test_stemmed
  res['topics'] = []
  res['net_scores'] = {
    'keywords_given_keywords': base_result(),
    'keywords_given_topic': base_result(),
    'input': base_result(),
    'topic': base_result(),
  }
  # convert stemmed input to bag of words (bow) and feed to model, sort topic mixture by the descending probability
  doc_topics = sorted(get_doc_topics(ldamodel, dictionary.doc2bow(test_stemmed)), key=lambda x: (x[1]), reverse=True)
  # unpack topic number and probability from topics
  for i, (topic_num, prob_topic) in enumerate(doc_topics):
    # ignore small probabilities
    if prob_topic > threshold:
      # gram top n keywords
      wp = ldamodel.show_topic(topic_num, topn=num_keywords)
      current_topic = {
        'dominant': i == 0,
        'topic_num': topic_num,
        'topic_keywords': wp,
        'probability': prob_topic,
        'scores': {
          'keywords_given_keywords': score_keywords_given_keywords([word for word, prop in wp], wp),
          'keywords_given_topic': score_keywords_given_topic([word for word, prop in wp], ldamodel.get_topics()[topic_num]),
          'input': score_input(test_stemmed, ldamodel.get_topics()[topic_num]),
          'topic': score_topic(ldamodel.get_topics()[topic_num])
        }
      }
      res['net_scores']['keywords_given_keywords'] = add_scores(res['net_scores']['keywords_given_keywords'], scale_scores(prob_topic, current_topic['scores']['keywords_given_keywords']))
      res['net_scores']['keywords_given_topic']    = add_scores(res['net_scores']['keywords_given_topic'], scale_scores(prob_topic, current_topic['scores']['keywords_given_topic']))
      res['net_scores']['input']                   = add_scores(res['net_scores']['input'], scale_scores(prob_topic, current_topic['scores']['input']))
      res['net_scores']['topic']                   = add_scores(res['net_scores']['topic'], scale_scores(prob_topic, current_topic['scores']['topic']))
      res['topics'].append(current_topic)
  return res