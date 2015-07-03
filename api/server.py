import sys
import os

proj_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(proj_path)
import json
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
app.config["CORS_HEADERS"] = 'Content-Type'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/modeltype/list")
def list_types():
    """Return list of types
    """
    #builtin_types = ArchivableType.list_types(serialized=True)
    builtin_types = {}
    print 'builtin_types is {}'.format(builtin_types)
    #json_str = json.dumps(builtin_types, indent=4, cls=ArchiverEncoder)
    json_str = "To be implemented"
    return json_str

@app.route("/api/modeltype/create", methods=["POST"])
def create_modeltype(): 
    """Create a new modeltype
    """
    data = request.get_json(force=True)
    fields = data["fields"]
    print fields
    return "Success"

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5500, debug=True)
