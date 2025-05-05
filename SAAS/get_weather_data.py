import pandas as pd
import datetime as dt
import requests
import argparse 
import os
import time
from datetime import datetime, timedelta

API_KEY = ""
REGIONS_DICTIONARY_FILE = "data/regions.csv"
OUTPUT_FOLDER = "data/weather_for_24_hours"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

df_regions = pd.read_csv(REGIONS_DICTIONARY_FILE)

parser = argparse.ArgumentParser(description='Отримати погодні дані на 12 годин')
parser.add_argument('--region', type=str, default='Донеччина', help='Регіон для прогнозу погоди')
args = parser.parse_args()

region = args.region
today_date = datetime.now().strftime("%Y-%m-%d")
country = "Ukraine"

city = df_regions[df_regions["region_alt"] == region]["center_city_en"].values[0]
location = f"{city},{country}"

file_name = f"weather_data_{city}.csv"
output_path = f"{OUTPUT_FOLDER}/{file_name}"

url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{today_date}/{today_date}?key={API_KEY}&include=hours"

print("URL:", url)
response = requests.get(url)
print("Status code:", response.status_code)

if response.status_code != 200:
    print(response.text)
else:
    try:
        data = response.json()
        
        if "days" not in data:
            print("Помилка: дані не містять інформації про дні")
            print(data)
        else:
            day_data = data["days"][0]
            
            day_base = {
                'day_tempmax': day_data.get('tempmax'),
                'day_tempmin': day_data.get('tempmin'),
                'day_temp': day_data.get('temp'),
                'day_dew': day_data.get('dew'),
                'day_humidity': day_data.get('humidity'),
                'day_precip': day_data.get('precip'),
                'day_precipcover': day_data.get('precipcover'),
                'day_solarradiation': day_data.get('solarradiation'),
                'day_solarenergy': day_data.get('solarenergy'),
                'day_uvindex': day_data.get('uvindex'),
                'day_sunrise': day_data.get('sunrise'),
                'day_sunset': day_data.get('sunset'),
                'day_moonphase': day_data.get('moonphase'),
                'day_datetime_timestamp': int(time.mktime(datetime.strptime(day_data.get('datetime'), '%Y-%m-%d').timetuple()))
            }
            
            def convert_time_to_decimal(time_str):
                if isinstance(time_str, str):
                    hours, minutes, seconds = map(int, time_str.split(':'))
                    decimal_time = hours + minutes/60 + seconds/3600
                    return decimal_time
                else:
                    return time_str
            
            day_base['day_sunrise'] = convert_time_to_decimal(day_base['day_sunrise'])
            day_base['day_sunset'] = convert_time_to_decimal(day_base['day_sunset'])
            
            hour_data = day_data.get('hours', [])
            
            all_hours_data = []
            
            for hour in hour_data:
                hour_record = day_base.copy()  
                
                hour_record.update({
                    'hour_temp': hour.get('feelslike'),
                    'hour_precipprob': hour.get('precipprob'),
                    'hour_snow': hour.get('snow'),
                    'hour_windgust': hour.get('windgust'),
                    'hour_windspeed': hour.get('windspeed'),
                    'hour_winddir': hour.get('winddir'),
                    'hour_pressure': hour.get('pressure'),
                    'hour_cloudcover': hour.get('cloudcover'),
                    'hour_visibility': hour.get('visibility', 16.970820946585334),  
                    'weather_Clear': 1 if hour.get('conditions') == 'Clear' else 0
                })
                
                all_hours_data.append(hour_record)
            
            df_hourly = pd.DataFrame(all_hours_data)
            
            columns_order = ['day_datetime_timestamp', 'day_tempmax', 'day_tempmin', 'day_temp',
                        'hour_temp', 'day_dew', 'day_humidity', 'day_precip', 'hour_precipprob',
                        'day_precipcover', 'hour_snow', 'hour_windgust', 'hour_windspeed',
                        'hour_winddir', 'hour_pressure', 'hour_cloudcover', 'hour_visibility',
                        'day_solarradiation', 'day_solarenergy', 'day_uvindex', 'day_sunrise',
                        'day_sunset', 'day_moonphase', 'weather_Clear']
            
            for col in columns_order:
                if col not in df_hourly.columns:
                    df_hourly[col] = None
            
            df_hourly = df_hourly[columns_order]
            
            df_hourly.to_csv(output_path, sep=';', encoding='utf-8', index=False)
            print(f"Збережено прогноз погоди на 12 годин у файл: {output_path}")
            print(f"Кількість рядків: {len(df_hourly)}")
            
    except Exception as e:
        print(f"Помилка при обробці даних: {e}")
        print(response.text[:500])