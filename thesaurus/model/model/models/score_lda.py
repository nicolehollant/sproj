import json
from model.config import stopwords, tokenizer, p_stemmer, all_scores, ldamodel, dictionary
import numpy as np
from functools import singledispatch

# https://ellisvalentiner.com/post/serializing-numpyfloat32-json/ needed help serializing numpy's sketchy floats lol
@singledispatch
def to_serializable(val):
  """Used by default."""
  return str(val)

@to_serializable.register(np.float32)
def ts_float32(val):
  """Used if *val* is an instance of numpy.float32."""
  return np.float64(val)

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

def get_doc_topics(lda, bow):
  gamma, _ = lda.inference([bow])
  topic_dist = gamma[0] / sum(gamma[0])  # normalize distribution
  return [(topicid, topicvalue) for topicid, topicvalue in enumerate(topic_dist)]

def get_topic(topic_num):
  topics = ldamodel.get_topics()
  if topic_num < len(topics):
    return { dictionary[i]: float(prob) for (i, prob) in enumerate(topics[topic_num]) }
  return None

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
  return json.loads(json.dumps(res, default=to_serializable)) # the tried and true parse(stringify)