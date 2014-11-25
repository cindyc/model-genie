import sys
import os

proj_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(proj_path)
import json
from flask import Flask, jsonify
from modelgenie.base import ArchivableType
from modelgenie.archiver import ArchiverEncoder

app = Flask(__name__)


@app.route('/type')
def list_types():
    """Return list of types
    """
    builtin_types = ArchivableType.list_types(serialized=True)
    print 'builtin_types is {}'.format(builtin_types)
    json_str = json.dumps(builtin_types, indent=4, cls=ArchiverEncoder)
    return json_str

if __name__ == '__main__':
    app.run(debug=True)
