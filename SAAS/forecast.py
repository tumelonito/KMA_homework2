import json
from flask import Flask, render_template


app = Flask(__name__)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


def check_token(token: str):
    if token is None:
        raise InvalidUsage("token is required", status_code=400)

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)


@app.route("/")
def home_page():
    return render_template('index.html')


@app.route("/content/api/v1/alarm_prediction", methods=["GET"])
def alarm_prediction():
    res = json.load(open("data/prediction.json"))
    return res

if __name__ == '__main__':
    app.run(debug=True)
