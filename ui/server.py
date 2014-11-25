from flask import Flask, render_template
import sys
import os

proj_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(proj_path)

from modelgenie.base import ArchivableModel

app = Flask(__name__)


@app.route('/')
def index():
    """Return list of builtin types
    """
    builtin_types = ArchivableModel.list_types()
    print 'builtin_types is {}'.format(builtin_types)
    return render_template('index.html', types=builtin_types)

if __name__ == '__main__':
    app.run(debug=True)
