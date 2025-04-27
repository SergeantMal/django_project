// Конфигурация
const DEFAULT_CITY = 'Москва';  // Город по умолчанию

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
        document.getElementById('cityText').textContent = city !== DEFAULT_CITY ? DEFAULT_CITY : 'Ошибка';
        if (city !== DEFAULT_CITY) {
            getWeather(DEFAULT_CITY);
        }
    }
}

// Функция определения местоположения по IP
async function detectLocation() {
    try {
        const response = await fetch('/detect-location');
        const data = await response.json();
        return data.city || DEFAULT_CITY;
    } catch (error) {
        console.log('Не удалось получить местоположение по IP:', error);
        return DEFAULT_CITY;
    }
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

// Переключение видимости виджета
document.getElementById('toggleWeather').addEventListener('click', () => {
    const container = document.querySelector('.weather-widget-container');
    container.classList.toggle('open');
});



