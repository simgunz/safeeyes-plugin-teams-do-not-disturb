#import appdirs
import flask
from flask_cors import CORS
from pathlib import Path

app = flask.Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def hello_world():
    if flask.request.method == 'POST':
        status = flask.request.json['status']
        write_status_to_file(status)
        return "ok"

def write_status_to_file(status):
    #safeeyes_presence_file = Path(appdirs.user_data_dir()) / "safeeyes" / "teamspresence"
    safeeyes_presence_file = Path().home() / ".local" / "share" / "safeeyes" / "teamspresence"
    safeeyes_presence_file.parent.mkdir(exist_ok=True)
    safeeyes_presence_file.write_text(status)
