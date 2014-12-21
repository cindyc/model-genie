from flask import Flask, render_template
import sys
import os

proj_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(proj_path)

from modelgenie.base import ModelGenie

app = Flask(__name__)


@app.route('/')
def index():
    """Return list of builtin types
    """
    return render_template('form.html')

#@app.route('/static/<path:static_file>')
#@app.route('/css/<path:static_file>')
def static_proxy(static_file):
    # send_static_file will guess the correct MIME type
    print 'Returning {}'.format(os.path.join('static', 'css', static_file))
    return app.send_static_file(os.path.join('static', 'css', static_file))

if __name__ == '__main__':
    app.run(debug=True)
