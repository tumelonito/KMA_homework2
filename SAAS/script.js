document.addEventListener('DOMContentLoaded', () => {
    const predictionDataElement = document.getElementById('prediction-data');
    const refreshButton = document.getElementById('refresh-button');
    const apiEndpoint = ''; // API endpoint

    // Функція для отримання та відображення даних
    const fetchAndDisplayPredictions = async () => {
        predictionDataElement.innerHTML = '<p>Завантаження прогнозу...</p>'; 

        try {
            const response = await fetch(apiEndpoint);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            predictionDataElement.innerHTML = ''; // Очистити повідомлення про завантаження

            if (data && data.regions_forecast && data.regions_forecast.length > 0) {
                const now = new Date();
                const currentHour = now.getHours(); // Отримуємо поточну годину (0-23)

                data.regions_forecast.forEach(regionData => {
                    const regionName = Object.keys(regionData)[0];
                    const predictions = regionData[regionName];

                    const regionCardDiv = document.createElement('div');
                    regionCardDiv.classList.add('region-card');

                    const regionNameElement = document.createElement('h2');
                    regionNameElement.classList.add('region-name');
                    regionNameElement.textContent = regionName;
                    regionCardDiv.appendChild(regionNameElement);

                    const hourlyForecastDiv = document.createElement('div');
                    hourlyForecastDiv.classList.add('hourly-forecast');

                    for (let i = 0; i < 24; i++) {
                        const hourKey = `${i < 10 ? '0' : ''}${i}:00`;
                        const isAlarm = predictions[hourKey];

                        const hourColumnDiv = document.createElement('div');
                        hourColumnDiv.classList.add('hour-column');

                        // Підсвічуємо колонку поточної години
                        if (i === currentHour) {
                            hourColumnDiv.classList.add('current-hour');
                        }

                        const hourLabelDiv = document.createElement('div');
                        hourLabelDiv.classList.add('hour-label');
                        hourLabelDiv.textContent = hourKey;
                        hourColumnDiv.appendChild(hourLabelDiv);

                        const predictionBlockDiv = document.createElement('div');
                        predictionBlockDiv.classList.add('prediction-block');

                        if (isAlarm) {
                            predictionBlockDiv.classList.add('alarm-true');
                            predictionBlockDiv.title = `${hourKey}: Прогнозується тривога`;
                        } else {
                            predictionBlockDiv.classList.add('alarm-false');
                            predictionBlockDiv.title = `${hourKey}: Тривога не прогнозується`;
                        }

                        hourColumnDiv.appendChild(predictionBlockDiv);
                        hourlyForecastDiv.appendChild(hourColumnDiv);
                    }

                    regionCardDiv.appendChild(hourlyForecastDiv);
                    predictionDataElement.appendChild(regionCardDiv);
                });
            } else {
                predictionDataElement.textContent = 'Дані прогнозу недоступні.';
            }
        } catch (error) {
            console.error('Помилка завантаження даних прогнозу:', error);
            predictionDataElement.textContent = 'Помилка завантаження прогнозу. Будь ласка, спробуйте пізніше.';
        }
    };

    // Завантажити дані при завантаженні сторінки
    fetchAndDisplayPredictions();

    // Додати обробник події для кнопки оновлення
    refreshButton.addEventListener('click', fetchAndDisplayPredictions);
});