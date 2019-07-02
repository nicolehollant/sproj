from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import os

MONGOPORT = os.getenv('MONGOPORT', "POOP")
database = os.getenv('database', "database")

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'notesBackend'
app.config['MONGO_URI'] = f'mongodb://{str(database)}:{str(MONGOPORT)}/notesBackend'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def get_default():
  return jsonify({'result' : "Sproj backend!"})

@app.route('/api/', methods=['GET'])
def get_api():
    result = {
        "Welcome Message": "Welcome to the thesaurus API",
        "Usage": "GET schtuff"
    }
    return jsonify({'result' : result})

if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0')