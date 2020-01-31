# from sklearn.decomposition import LatentDirichletAllocation
# from sklearn.datasets import make_multilabel_classification
# # This produces a feature matrix of token counts, similar to what
# # CountVectorizer would produce on text.
# X, _ = make_multilabel_classification(random_state=0)
# lda = LatentDirichletAllocation(n_components=5,
#     random_state=0)
# lda.fit(X)

# # get topics for some given samples:
# print(lda.transform(X[-2:]))
# print(X)


"""
from https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html
"""
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from scipy.sparse import csc

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
    
# create sample documents
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
doc_e = "Health professionals say that brocolli is good for your health." 

test = tokenizer.tokenize("Some health experts suggest that driving my brother to eat good brocolli does better".lower())
test_stopped = [i for i in test if not i in en_stop]
test_stemmed = [p_stemmer.stem(i) for i in test_stopped]

# compile sample documents into a list
doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:
    
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    
    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    
    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word = dictionary, passes=20)
print(dictionary.token2id["brocolli"], dictionary.token2id["health"])

# {list of list of (int, float), scipy.sparse.csc}
# print("inference", ldamodel.inference([[
#   [dictionary.token2id["brocolli"], 0.5],
#   [dictionary.token2id["health"], 0.5],
# ], 'asd'], True))
# ldamodel.print_topic
# print(ldamodel.print_topics(num_topics=3, num_words=3))
# print(ldamodel.print_topics())

for i, row in enumerate(ldamodel[[dictionary.doc2bow(test_stemmed)]]):
# for i, row in enumerate(ldamodel[corpus]):
  row = sorted(row, key=lambda x: (x[1]), reverse=True)
  # Get the Dominant topic, Perc Contribution and Keywords for each document
  for j, (topic_num, prop_topic) in enumerate(row):
    if j == 0:  # => dominant topic
      wp = ldamodel.show_topic(topic_num)
      topic_keywords = ", ".join([word for word, prop in wp])
      print(wp, "\n\t", topic_keywords)

# def format_topics_sentences(ldamodel=lda_model, corpus=corpus, texts=data):
#     # Init output
#     sent_topics_df = pd.DataFrame()

#     # Get main topic in each document
#     for i, row in enumerate(ldamodel[corpus]):
#         row = sorted(row, key=lambda x: (x[1]), reverse=True)
#         # Get the Dominant topic, Perc Contribution and Keywords for each document
#         for j, (topic_num, prop_topic) in enumerate(row):
#             if j == 0:  # => dominant topic
#                 wp = ldamodel.show_topic(topic_num)
#                 topic_keywords = ", ".join([word for word, prop in wp])
#                 sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
#             else:
#                 break
#     sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

#     # Add original text to the end of the output
#     contents = pd.Series(texts)
#     sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
#     return(sent_topics_df)


# df_topic_sents_keywords = format_topics_sentences(ldamodel=optimal_model, corpus=corpus, texts=data)
