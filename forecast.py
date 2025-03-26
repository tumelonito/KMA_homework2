import requests
import datetime as dt
from flask import Flask, request

API_TOKEN = "<TOKEN>"
API_KEY_WEATHER = "<KEY>"
API_KEY_ALARMS = "<KEY>"

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


"""
Check if token is valid,
else raises an exception.
"""
def check_token(token: str):
    if token is None:
        raise InvalidUsage("token is required", status_code=400)

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)


@app.route("/")
def home_page():
    return "<p><h2>KMA Homework2: python Saas.</h2></p>"


@app.route("/content/api/v1/weather_forecast", methods=["POST"])
def weather_forecast():
    start_dt = dt.datetime.now()
    json_data = request.get_json()

    token = json_data.get("token")
    check_token(token)

    if json_data.get("location"):
        location = json_data.get("location")
    else:
        raise InvalidUsage("location is required", status_code=400)

    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" + location

    response = requests.get(url, params={'key': API_KEY_WEATHER, 'unitGroup': 'metric'})

    if response.status_code != requests.codes.ok:
        raise InvalidUsage(response.text, status_code=response.status_code)

    end_dt = dt.datetime.now()

    result = {
        "event_start_datetime": start_dt.isoformat(),
        "event_finished_datetime": end_dt.isoformat(),
        "event_duration": str(end_dt - start_dt),
        "weather_forecast": response.json()
    }
    return result


@app.route("/content/api/v1/active_alerts", methods=["POST"])
def active_alerts():
    start_dt = dt.datetime.now()
    json_data = request.get_json()

    token = json_data.get("token")
    check_token(token)

    url = f"https://api.alerts.in.ua/v1/alerts/active.json"
    response = requests.get(url, params={'token': API_KEY_ALARMS})

    end_dt = dt.datetime.now()

    result = {
        "event_start_datetime": start_dt.isoformat(),
        "event_finished_datetime": end_dt.isoformat(),
        "event_duration": str(end_dt - start_dt),
    }
    result.update(response.json())

    return result
