from . import routes
from model.config import *
from model.models.score import *

@routes.route('/score/', methods=["GET"])
def get_score():
  return jsonify({
    "message": "this is a test for the score endpoint"
  }), 200

@routes.route('/score/', methods=["POST"])
def post_score():
  reqbody = request.get_json()
  text = reqbody.get("text", "")

  if text.strip() == "":
    return jsonify({
      'message': 'Empty text value'
    }), 400
  
  ignore = reqbody.get("ignore", None)
  score_model = Score(ignoreArticles=ignore)
  out = score_model.score_body(text)

  return jsonify({
    "message": "success!",
    "data": out
  }), 200

@routes.route('/make-affect/', methods=["GET"])
def get_make_affect():
  return jsonify({
    "message": "this is a test for the make_affect endpoint"
  }), 200

@routes.route('/make-affect/<affect>', methods=["POST"])
def post_make_affect(affect):
  reqbody = request.get_json()
  text = reqbody.get("text", "")

  if text.strip() == "":
    return jsonify({
      'message': 'Empty text value'
    }), 400
  
  score_model = Score(ignoreArticles=True)
  out = score_model.make_affect(text, affect)

  if out is None:
    return jsonify({
      'message': 'Bad affect value, choose amoung: sadness, joy, fear, anger'
    }), 400

  return jsonify({
    "message": "success!",
    "data": out
  }), 200
  


  

  