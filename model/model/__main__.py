from model.config import *
from model.endpoints import routes

app.url_map.strict_slashes = False
app.register_blueprint(routes)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"message": "Oops! Doesnt exist"}), 404

app.run(host='0.0.0.0', port=5000)