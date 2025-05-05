import datetime as dt
import pickle
import nltk
import re
import scipy
import sys
import pytz
import json
import os
import ssl
import numpy as np
import pandas as pd
import requests
from utils.get_weather import get_weather_for_12_hours
from scipy import sparse
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD
from tqdm import tqdm

from utils import get_weather
from utils import text_processing

chunks = pd.read_csv('Data/vectors_df.csv', chunksize=500)
try:
    vectors_df = pd.concat(chunks)
except MemoryError:
    print("No data available due to memory error.")


tfidf = pickle.load(open("models/trained_gradient_boosting_1.0.pkl", "rb"))
cv = pickle.load(open("models/trained_knn_1.8.pkl", "rb"))
model = pickle.load(open("models/trained_knn_1.8.pkl", "rb"))


cities = ['Kyiv', 'Kharkiv', 'Lviv', 'Odesa', 'Donetsk', 'Luhansk', 'Kherson', 'Simferopol', 'Mykolaiv', 'Chernihiv', 'Dnipro', 'Vinnytsia', 'Zhytomyr', 'Kropyvnytskyi', 'Poltava', 'Sumy', 'Rivne', 'Khmelnytskyi', 'Cherkasy', 'Uzhgorod', 'Zaporozhye', 'Ivano-Frankivsk']
date = dt.datetime.now(pytz.timezone('Europe/Kiev'))
result = {}

total_iterations = 100
with tqdm(total=total_iterations) as pbar:
    for _ in range(total_iterations):
        for city in cities:
            pbar.set_description(f'Processing {city}')
            df_weather_complete = get_weather_for_12_hours(city, date)
            if df_weather_complete is not None:
                # Об'єднання даних
                df_weather_complete['key'] = 1
                vectors_df['key'] = 1  
                df_all = df_weather_complete.merge(vectors_df, how='left', left_on='key', right_on='key')
                
                # Видалення зайвих стовпців
                to_drop = ['key', 'date', 'date_tomorrow_datetime', 'keywords', 'main_text']
                if 'sunrise' in df_all.columns:
                    exceptions = ['sunset', 'sunrise']
                    to_drop.extend(exceptions)
                df_all = df_all.drop(to_drop, axis=1)
                
                # Вибір необхідних стовпців
                df_all = df_all[['Unnamed: 0', 'day_tempmax', 'day_tempmin', 'day_temp', 'day_dew', 'day_humidity', 'day_precip', 'day_precipcover', 'day_solarradiation', 'day_solarenergy', 'day_uvindex', 'day_moonphase', 'hour_datetimeEpoch', 'hour_temp', 'hour_humidity', 'hour_dew', 'hour_precipprob', 'hour_snow', 'hour_snowdepth', 'hour_windgust', 'hour_windspeed', 'hour_winddir', 'hour_pressure', 'hour_visibility', 'hour_cloudcover', 'hour_severerisk']]
                
                # Завантаження матриці з NPZ файлу
                df_weather_matrix = scipy.sparse.load_npz('Data/weather_alarms_tfidf_features.npz')
                
                # Створення розрідженої матриці
                df_weather_matrix_csr = scipy.sparse.csr_matrix(df_weather_matrix)  
                df_all_data_csr = scipy.sparse.hstack((df_weather_matrix_csr, df_weather_matrix), format='csr')
                
                # Прогнозування
                predicted = model.predict(df_all_data_csr) 
                
                # Створення словника результатів
                hours = [(date + dt.timedelta(hours=i)).replace(minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M') for i in range(12)]
                result[city] = dict(zip(hours, predicted))
            else:
                print(f"No data available for {city} at the moment.")
            
            pbar.update(1)  # оновлюємо значення лічильника

# Результат
result

        
result = pd.DataFrame(result)
VERSION = "1"
result.to_csv(f'results_{VERSION}.txt', sep='\t', index=False)