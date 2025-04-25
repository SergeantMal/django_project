
    // Конфигурация
    const DEFAULT_CITY = 'Москва';  // Пример города по умолчанию

    // Функция для обновления интерфейса погоды
    function updateWeather(data) {
        const current = data.current;

        document.getElementById('cityText').textContent = data.location.name;
        document.getElementById('temperature').textContent = `${Math.round(current.temp_c)}°`;
        document.getElementById('weatherCondition').textContent = current.condition.text;

        // Используем иконку из API
        const iconUrl = `https:${current.condition.icon}`;
        const iconContainer = document.getElementById('weatherIcon');
        iconContainer.innerHTML = `<img src="${iconUrl}" alt="${current.condition.text}">`;
    }

    // Функция получения данных о погоде
    async function getWeather(city) {
        try {
            const response = await fetch(`/api/weather/${encodeURIComponent(city)}`);
            const data = await response.json();

            if (data.error) throw new Error(data.error);
            updateWeather(data);
        } catch (error) {
            console.error('Ошибка:', error);
            if (city !== DEFAULT_CITY) {
                getWeather(DEFAULT_CITY);
            } else {
                document.getElementById('cityText').textContent = 'Ошибка';
            }
        }
    }


    // Функция для получения местоположения по GPS
    async function detectLocationFromGPS() {
        return new Promise((resolve, reject) => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    async (position) => {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;

                        try {
                            // Получение города через географические координаты
                            const response = await fetch(`https://geocode.xyz/${lat},${lon}?geoit=json`);
                            const data = await response.json();
                            if (data.city) {
                                resolve(data.city);
                            } else {
                                reject('Не удалось определить город по GPS');
                            }
                        } catch (error) {
                            reject('Ошибка при получении города по GPS');
                        }
                    },
                    (error) => {
                        reject('Ошибка доступа к GPS');
                    }
                );
            } else {
                reject('Геолокация не поддерживается');
            }
        });
    }

    // Функция определения местоположения (сначала GPS, потом IP)
    async function detectLocation() {
        try {
            // Пробуем получить местоположение по GPS
            const gpsLocation = await detectLocationFromGPS();
            return gpsLocation;
        } catch (error) {
            console.log('Не удалось получить местоположение по GPS:', error);
            // Если не удалось, используем IP для определения местоположения
            return await detectLocationByIP();
        }
    }

    // Функция определения местоположения по IP
    async function detectLocationByIP() {
        try {
            const response = await fetch('/detect-location');
            const data = await response.json();

            if (data.city) {
                return data.city;
            }
        } catch (error) {
            console.log('Не удалось получить местоположение по IP:', error);
        }

        return DEFAULT_CITY;
    }

    // Клик по городу - обновление данных
    document.getElementById('cityName').addEventListener('click', async () => {
        const city = await detectLocation();
        getWeather(city);
    });

    // Инициализация виджета
    async function initWidget() {
        const city = await detectLocation();
        getWeather(city);
    }

    // Запуск виджета
    initWidget();
    document.getElementById('toggleWeather').addEventListener('click', () => {
    const container = document.querySelector('.weather-widget-container');
    container.classList.toggle('open');
    });




