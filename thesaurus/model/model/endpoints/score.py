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
  


  

  