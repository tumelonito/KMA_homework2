import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import pickle
import json
import pandas as pd
import subprocess
import datetime as dt
import sqlite3


def run_notebook(path):
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)
        
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb)


def merge_data(city):
    weather = pd.read_csv(f"data/weather_for_24_hours/weather_data_{city}.csv", sep=';')
    isw_repeated = pd.concat([isw] * len(weather), ignore_index=True)

    merged = pd.concat([weather.reset_index(drop=True), isw_repeated.reset_index(drop=True)], axis=1)

    if 'date' in merged.columns:
        merged = merged.drop(columns=['date'])

    return merged


def process_prediction(prediction):
    res = {}
    for hour in range(24):
        formatted_hour = f"{hour:02d}:00"
        res[formatted_hour] = bool(prediction[hour])
    return res


def predict_with_model(test_data, model):
    processed_data_scaled = test_data

    prediction = model.predict(processed_data_scaled)
    prediction_proba = model.predict_proba(processed_data_scaled)

    return prediction, prediction_proba


regions = pd.read_csv('data/regions.csv')
regions = regions.drop(regions[regions["region_alt"] == "Луганщина"].index)
regions = regions.drop(regions[regions["region_alt"] == "Крим"].index)

for region in regions["region_alt"]:
    subprocess.run(['python', 'get_weather_data.py', '--region', region])

run_notebook('parse_isw.ipynb')
isw = pd.read_csv("data/isw_latest_report.csv",sep=';')

ml_model = pickle.load(open('xgboost_model.pkl', 'rb'))


res = {
    "last_model_train_time" : '2025-04-27T09:36:51.635093',
    "last_prediction_time" : dt.datetime.now().isoformat(),
    "regions_forecast" : []
}

for city in regions["center_city_en"]:
    merged = merge_data(city)
    prediction, prediction_proba = predict_with_model(merged, ml_model)
    res['regions_forecast'].append({city: process_prediction(prediction)})
    
file_path = 'data/prediction.json'
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(res, f, indent=4, ensure_ascii=False)

conn = sqlite3.connect('data/predictions.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS forecasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        hour TEXT,
        prediction INTEGER,
        last_model_train_time TEXT
    )
''')

for region_dict in res["regions_forecast"]:
    for city, forecast in region_dict.items():
        for hour, value in forecast.items():
            cursor.execute('''
                INSERT INTO forecasts (city, hour, prediction, last_model_train_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                city,
                hour,
                int(value),
                res["last_model_train_time"],
                res["last_prediction_time"]
            ))

conn.commit()
conn.close()
