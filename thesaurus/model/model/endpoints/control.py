from . import routes
from model.config import *
from model.models.control import *

@routes.route('/control/', methods=["GET"])
def get_control():
  return jsonify({
    "message": "this is a test for the control endpoint"
  }), 200

@routes.route('/control/', methods=["POST"])
def post_control():
  reqbody = request.get_json()
  text = reqbody.get("text", "")

  if text.strip() == "":
    return jsonify({
      'message': 'Empty text value'
    }), 400
  
  prob = reqbody.get("prob", None)
  ignore = reqbody.get("ignore", None)
  control = Control(prob=prob, ignoreArticles=ignore)
  out, notPresent, numChanged, stopwordsSkipped = control.replaceWords(text)
  return jsonify({
    "message": "success!",
    "data": {
      "input": text,
      "output": ' '.join(out),
      "notPresent": notPresent,
      "stopwordsSkipped": stopwordsSkipped,
      "numChanged": numChanged
    }
  }), 200
  


  

  