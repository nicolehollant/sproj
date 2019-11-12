import os
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from bson import json_util
from dotenv import load_dotenv
# from nltk.corpus import stopwords as nltk_stopwords


from model.utils import *
# from model.models import *

load_dotenv()
app = Flask(__name__)
CORS(app)

routes = Blueprint('routes', __name__)

# stopwords = ['a', 'and', 'the', 'an', 'to', 'is', 'be']
# stopwords = set(nltk_stopwords.words('english'))
stopwords = ['ve', 'won', 'more', 'needn', "doesn't", 'most', 'each', 'down', 'should', "weren't", 'yourself', "didn't", 'on', 'below', 'whom', 'herself', 'your', "you'd", 'hers', 'you', 'about', 'because', 'up', 'me', 'can', 'out', "hasn't", 'him', 'again', 'is', 'same', 'were', 'a', "wasn't", 'd', "haven't", 'them', 'very', 'i', 'such', 'mightn', 'until', "mustn't", 'haven', 'off', 'here', 'it', 'isn', "won't", 'over', "that'll", 'the', "hadn't", 'wouldn', 'yourselves', 'was', 'we', 'both', 'doesn', 'been', 'when', "wouldn't", 'only', 'aren', 'has', 'why', 'do', 'weren', 'at', 't', 'from', 'how', 's', 'these', 'for', 'be', 'through', 'ourselves', 'to', 'where', 'of', "you're", 'in', 'he', "aren't", "shouldn't", "you'll", 'nor', 'didn', 'above', 'couldn', 'himself', 'than', 'hasn', 'they', 'so', 'm', 'but', 'other', "couldn't", 'll', 'its', 'then', 'there', 'some', 'too', 'shan', 'no', "she's", 'wasn', 're', 'hadn', 'being', 'what', 'this', 'are', 'our', 'myself', 'she', 'and', "isn't", 'does', 'that', 'while', 'own', 'having', 'against', 'had', 'by', 'their', 'my', 'did', 'shouldn', 'during', 'ma', 'now', 'or', 'into', 'few', 'themselves', 'once', "don't", 'her', 'any', 'will', 'ours', 'further', 'his', 'with', "shan't", "should've", 'just', 'after', "you've", 'yours', 'between', 'before', 'itself', 'theirs', 'ain', 'those', 'am', 'not', 'all', 'o', "mightn't", 'which', "it's", "needn't", 'who', 'under', 'y', 'mustn', 'if', 'have', 'an', 'doing', 'as', 'don']

# dburi = os.environ.get('DBURI')
# if not dburi:
#   print("Running locally")
#   dburi = "mongodb://localhost:27017/thesaurus"

# app.config['MONGO_URI'] = dburi
# mongo = PyMongo(app)