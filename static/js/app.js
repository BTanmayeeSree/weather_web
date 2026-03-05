class WeatherApp {
    constructor() {
        this.currentWeatherData = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadWeatherData();
    }

    bindEvents() {
        const searchBtn = document.getElementById('search-btn');
        const searchInput = document.getElementById('search-input');
        const refreshBtn = document.getElementById('refresh-btn');

        searchBtn.addEventListener('click', () => this.handleSearch());
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSearch();
        });
        refreshBtn.addEventListener('click', () => this.loadWeatherData());
    }

    async handleSearch() {
        const searchInput = document.getElementById('search-input');
        const city = searchInput.value.trim();
        
        if (!city) {
            this.showError('Please enter a city name');
            return;
        }

        await this.loadWeatherData(city);
        searchInput.value = '';
    }

    async loadWeatherData(city = null) {
        this.showLoading(true);
        this.hideError();
        
        try {
            const url = city ? `/api/weather?city=${encodeURIComponent(city)}` : '/api/weather';
            const response = await fetch(url);
            const data = await response.json();

            if (data.success) {
                this.currentWeatherData = data;
                this.displayWeatherData(data);
                this.showWeatherContent(true);
            } else {
                this.showError(data.error || 'Failed to fetch weather data');
                this.showWeatherContent(false);
            }
        } catch (error) {
            this.showError('Network error. Please check your connection.');
            this.showWeatherContent(false);
        } finally {
            this.showLoading(false);
        }
    }

    displayWeatherData(data) {
        const current = data.current;
        const location = data.location;
        
        // Update main weather info
        document.getElementById('city-name').textContent = `${location.city}, ${location.country}`;
        document.getElementById('current-date').textContent = this.formatDate(new Date());
        document.getElementById('temperature').textContent = `${Math.round(current.main.temp)}°C`;
        document.getElementById('weather-description').textContent = current.weather[0].description;
        document.getElementById('feels-like').textContent = `${Math.round(current.main.feels_like)}°C`;
        document.getElementById('humidity').textContent = `${current.main.humidity}%`;
        document.getElementById('wind-speed').textContent = `${current.wind.speed} m/s`;
        document.getElementById('pressure').textContent = `${current.main.pressure} hPa`;
        document.getElementById('visibility').textContent = `${(current.visibility / 1000).toFixed(1)} km`;

        // Update weather icon
        this.updateWeatherIcon(current.weather[0].main, current.weather[0].icon);
        
        // Update background gradient based on weather
        this.updateBackgroundGradient(current.weather[0].main);
        
        // Update air quality
        if (data.pollution && data.pollution.list && data.pollution.list.length > 0) {
            const aqi = data.pollution.list[0].main.aqi;
            document.getElementById('air-quality').textContent = this.getAirQualityText(aqi);
        }

        // Display forecast
        this.displayForecast(data.forecast);
        
        // Display hourly forecast
        this.displayHourlyForecast(data.forecast);
    }

    updateWeatherIcon(weatherMain, iconCode) {
        const iconElement = document.getElementById('weather-icon');
        iconElement.className = 'fas';
        
        // Remove all animation classes
        iconElement.classList.remove('weather-icon-sunny', 'weather-icon-cloudy', 'weather-icon-rainy');
        
        switch (weatherMain.toLowerCase()) {
            case 'clear':
                iconElement.classList.add('fa-sun', 'weather-icon-sunny');
                break;
            case 'clouds':
                iconElement.classList.add('fa-cloud', 'weather-icon-cloudy');
                break;
            case 'rain':
                iconElement.classList.add('fa-cloud-rain', 'weather-icon-rainy');
                break;
            case 'drizzle':
                iconElement.classList.add('fa-cloud-rain', 'weather-icon-rainy');
                break;
            case 'thunderstorm':
                iconElement.classList.add('fa-bolt');
                break;
            case 'snow':
                iconElement.classList.add('fa-snowflake');
                break;
            case 'mist':
            case 'fog':
                iconElement.classList.add('fa-smog');
                break;
            default:
                iconElement.classList.add('fa-question');
        }
    }

    updateBackgroundGradient(weatherMain) {
        const body = document.body;
        body.className = 'min-h-screen';
        
        switch (weatherMain.toLowerCase()) {
            case 'clear':
                body.classList.add('sunny-gradient');
                break;
            case 'clouds':
                body.classList.add('cloudy-gradient');
                break;
            case 'rain':
            case 'drizzle':
                body.classList.add('rainy-gradient');
                break;
            case 'thunderstorm':
                body.classList.add('rainy-gradient');
                break;
            case 'snow':
                body.classList.add('gradient-snowy');
                break;
            default:
                body.classList.add('weather-gradient');
        }
    }

    displayForecast(forecastData) {
        const container = document.getElementById('forecast-container');
        container.innerHTML = '';
        
        // Group forecast by day
        const dailyForecasts = this.groupForecastByDay(forecastData.list);
        
        // Take next 5 days
        const next5Days = dailyForecasts.slice(0, 5);
        
        next5Days.forEach((day, index) => {
            const card = this.createForecastCard(day, index);
            container.appendChild(card);
        });
    }

    displayHourlyForecast(forecastData) {
        const container = document.getElementById('hourly-container');
        container.innerHTML = '';
        
        // Take next 24 hours
        const hourlyData = forecastData.list.slice(0, 8);
        
        hourlyData.forEach((hour, index) => {
            const card = this.createHourlyCard(hour, index);
            container.appendChild(card);
        });
    }

    createForecastCard(dayData, index) {
        const card = document.createElement('div');
        card.className = 'glass-morphism rounded-xl p-4 text-white text-center weather-card animate-fade-in';
        card.style.animationDelay = `${index * 0.1}s`;
        
        const date = new Date(dayData.date);
        const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
        const temp = Math.round(dayData.main.temp);
        const icon = this.getWeatherIcon(dayData.weather[0].main);
        
        card.innerHTML = `
            <div class="text-sm font-semibold mb-2">${dayName}</div>
            <div class="text-2xl mb-2">
                <i class="fas ${icon}"></i>
            </div>
            <div class="text-lg font-bold">${temp}°C</div>
            <div class="text-xs text-white/70 mt-1">${dayData.weather[0].description}</div>
        `;
        
        return card;
    }

    createHourlyCard(hourData, index) {
        const card = document.createElement('div');
        card.className = 'glass-morphism rounded-xl p-3 text-white text-center min-w-[100px] weather-card animate-fade-in';
        card.style.animationDelay = `${index * 0.05}s`;
        
        const time = new Date(hourData.dt * 1000);
        const hour = time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        const temp = Math.round(hourData.main.temp);
        const icon = this.getWeatherIcon(hourData.weather[0].main);
        
        card.innerHTML = `
            <div class="text-xs font-semibold mb-2">${hour}</div>
            <div class="text-xl mb-2">
                <i class="fas ${icon}"></i>
            </div>
            <div class="text-sm font-bold">${temp}°C</div>
        `;
        
        return card;
    }

    groupForecastByDay(forecastList) {
        const dailyData = {};
        
        forecastList.forEach(item => {
            const date = new Date(item.dt * 1000);
            const dateKey = date.toDateString();
            
            if (!dailyData[dateKey]) {
                dailyData[dateKey] = {
                    date: dateKey,
                    main: {
                        temp: item.main.temp,
                        temp_min: item.main.temp_min,
                        temp_max: item.main.temp_max
                    },
                    weather: [item.weather[0]],
                    list: []
                };
            }
            
            dailyData[dateKey].list.push(item);
            
            // Update min/max temperatures
            dailyData[dateKey].main.temp_min = Math.min(dailyData[dateKey].main.temp_min, item.main.temp_min);
            dailyData[dateKey].main.temp_max = Math.max(dailyData[dateKey].main.temp_max, item.main.temp_max);
        });
        
        return Object.values(dailyData);
    }

    getWeatherIcon(weatherMain) {
        switch (weatherMain.toLowerCase()) {
            case 'clear': return 'fa-sun';
            case 'clouds': return 'fa-cloud';
            case 'rain': return 'fa-cloud-rain';
            case 'drizzle': return 'fa-cloud-rain';
            case 'thunderstorm': return 'fa-bolt';
            case 'snow': return 'fa-snowflake';
            case 'mist':
            case 'fog': return 'fa-smog';
            default: return 'fa-question';
        }
    }

    getAirQualityText(aqi) {
        const levels = ['Good', 'Fair', 'Moderate', 'Poor', 'Very Poor'];
        return levels[aqi - 1] || 'Unknown';
    }

    formatDate(date) {
        return date.toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
    }

    showLoading(show) {
        const loadingElement = document.getElementById('loading');
        loadingElement.classList.toggle('hidden', !show);
    }

    showError(message) {
        const errorElement = document.getElementById('error');
        const errorMessage = document.getElementById('error-message');
        errorMessage.textContent = message;
        errorElement.classList.remove('hidden');
    }

    hideError() {
        const errorElement = document.getElementById('error');
        errorElement.classList.add('hidden');
    }

    showWeatherContent(show) {
        const contentElement = document.getElementById('weather-content');
        contentElement.classList.toggle('hidden', !show);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WeatherApp();
});

// Add some interactive features
document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K for search focus
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            document.getElementById('search-input').focus();
        }
        
        // Ctrl/Cmd + R for refresh
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            location.reload();
        }
    });
});
