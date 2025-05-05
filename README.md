# KMA: Air Threat Forecasting for Ukraine

## Overview

This project is a Python-based SaaS web application that analyzes and forecasts air alarms, explosions, and artillery activity across different regions of Ukraine. It combines machine learning, automated data collection, and regional intelligence to estimate threats and highlight potentially dangerous zones on a per-oblast basis.

## Motivation

Since the beginning of the full-scale invasion of Ukraine in 2022, the need for fast, accessible, and data-driven situational awareness has become critical. This project was born out of a desire to build a tool that can **assist civilians, researchers, and responders** in understanding where and when threats may emerge.

By aggregating and analyzing open-source intelligence such as reports from the [Institute for the Study of War (ISW)](https://understandingwar.org/), the system aims to **translate raw conflict data into actionable insight**. It also serves as an academic exercise, developed as part of coursework at the [National University of Kyiv-Mohyla Academy](https://www.ukma.edu.ua/eng/).

## Features

- 🔁 **Automated Data Collection**: Fetches and parses information from open intelligence sources like [ISW](https://understandingwar.org/) via scheduled scripts.
- 🧠 **Forecasting Models**: Employs machine learning models to predict the likelihood of future incidents such as air raids or shelling.
- 🌍 **Regional Intelligence**: Forecasts are localized to Ukrainian oblasts, providing more relevant data to users depending on their location.
- 📊 **Visualization-Ready Output**: Outputs are formatted for easy integration with dashboards and map-based visualizations.
- 🧩 **Modular Structure**: Easily extensible architecture — new sources, models, or logic modules can be added without significant restructuring.
- ☁️ **SaaS-Friendly Deployment**: Designed to run on modern cloud platforms using `uWSGI`, `Docker`, and optionally wrapped with `Flask` or `FastAPI` for API access.

## Project Structure

```
├── dataAnalysis/             # Data analysis utilities and exploratory notebooks
├── dataOperations/           # Scripts for loading and transforming raw datasets
├── isw_preparation/          # ISW-specific data collection logic
├── merge/                    # Dataset merging and unification
├── models/                   # Saved ML models and model helpers
├── train/                    # Model training scripts and configurations
├── collect_isw_data.ipynb    # Notebook for retrieving and exploring ISW data
├── forecast.py               # Core script for generating region-specific forecasts
├── requirements.txt          # Dependency list
└── README.md                 # You're reading it 🙂
```

## Installation

Make sure you have **Python 3.11+** installed.

```bash
git clone https://github.com/tumelonito/KMA_homework2.git
cd KMA_homework2
pip install -r requirements.txt
```

## Deployment Notes

This application is deployable as a lightweight SaaS system. You can run it locally or host it on cloud platforms like:

- [Railway](https://railway.app/)
- [Render](https://render.com/)
- [Heroku](https://www.heroku.com/)
- [AWS EC2 / Lightsail](https://aws.amazon.com/lightsail/)

You may optionally:

- Add a `Procfile` or `Dockerfile` for streamlined deployment.
- Use `uWSGI` or `gunicorn` as WSGI servers for production environments.

## Author

As part of academic work at the [National University of Kyiv-Mohyla Academy](https://www.ukma.edu.ua/eng/)


