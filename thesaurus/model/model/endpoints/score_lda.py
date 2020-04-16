from . import routes
from model.config import *
from model.models.score_lda import *

@routes.route('/lda/', methods=["GET"])
def get_score_lda():
  return jsonify({
    "message": "this is a test for the score endpoint"
  }), 200

@routes.route('/lda/topic/<topic_num>', methods=["GET"])
def get_topic_lda(topic_num):
  try:
    topic_num = int(topic_num)
    res = get_topic(topic_num)
    if res is None:
      return jsonify({
        'message': 'Out of bounds, maximum number is 100'
      }), 400
    return jsonify({
      "message": "success!",
      "data": res
    }), 200
  except:
    return jsonify({
      'message': 'NaN'
    }), 400

@routes.route('/lda/', methods=["POST"])
def post_score_lda():
  reqbody = request.get_json()
  text = reqbody.get("text", "")

  if text.strip() == "":
    return jsonify({
      'message': 'Empty text value'
    }), 400
  
  threshold = reqbody.get("threshold", 0.01)
  num_keywords = reqbody.get("num_keywords", 20)
  try:
    out = eval_text(text, num_keywords=num_keywords, threshold=threshold)
    return jsonify({
      "message": "success!",
      "data": out
    }), 200
  except:
    return jsonify({
      "message": "error! something went wrong",
    }), 400  