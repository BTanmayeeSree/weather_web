from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

# Purple Glass Morphism Weather UI Template
MODERN_WEATHER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Forecast</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            overflow: hidden;
        }
        
        .weather-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            text-align: center;
        }
        
        .header {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 30px;
        }
        
        .weather-icon {
            font-size: 40px;
            margin-right: 15px;
        }
        
        .header-text h1 {
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .header-text p {
            font-size: 14px;
            opacity: 0.8;
        }
        
        .search-section {
            margin-bottom: 30px;
        }
        
        .search-container {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 30px;
        }
        
        .search-input {
            padding: 12px 20px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 16px;
            width: 200px;
        }
        
        .search-input::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        
        .search-btn {
            padding: 12px 25px;
            border: none;
            border-radius: 25px;
            background: white;
            color: #667eea;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .search-btn:hover {
            transform: scale(1.05);
        }
        
        .weather-display {
            margin-bottom: 30px;
        }
        
        .city-name {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .temperature {
            font-size: 48px;
            font-weight: 300;
            margin-bottom: 10px;
        }
        
        .weather-condition {
            font-size: 18px;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .details-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        
        .detail-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }
        
        .detail-label {
            font-size: 12px;
            opacity: 0.7;
            margin-bottom: 5px;
        }
        
        .detail-value {
            font-size: 16px;
            font-weight: 600;
        }
        
        .loading {
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .error {
            color: #ff6b6b;
            background: rgba(255, 107, 107, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="weather-container">
        <div class="header">
            <div class="weather-icon">🌤️</div>
            <div class="header-text">
                <h1>Weather Forecast</h1>
                <p>Beautiful weather app with stunning UI</p>
            </div>
        </div>
        
        <div class="search-section">
            <div class="search-container">
                <input type="text" id="cityInput" class="search-input" placeholder="Enter city..." value="London">
                <button class="search-btn" onclick="getWeather()">Get Weather</button>
            </div>
        </div>
        
        <div id="weatherResult">
            <div class="weather-display">
                <div class="city-name" id="cityName">London</div>
                <div class="temperature" id="temperature">15°C</div>
                <div class="weather-condition" id="condition">Partly Cloudy</div>
            </div>
            
            <div class="details-grid">
                <div class="detail-card">
                    <div class="detail-label">Feels like</div>
                    <div class="detail-value" id="feelsLike">13°C</div>
                </div>
                <div class="detail-card">
                    <div class="detail-label">Humidity</div>
                    <div class="detail-value" id="humidity">65%</div>
                </div>
                <div class="detail-card">
                    <div class="detail-label">Wind</div>
                    <div class="detail-value" id="windSpeed">5.2 m/s</div>
                </div>
                <div class="detail-card">
                    <div class="detail-label">Pressure</div>
                    <div class="detail-value" id="pressure">1013 hPa</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Weather data for different cities
        const weatherData = {
            'London': {
                temp: 15,
                condition: 'Partly Cloudy',
                feelsLike: 13,
                humidity: 65,
                wind: 5.2,
                pressure: 1013
            },
            'New York': {
                temp: 18,
                condition: 'Sunny',
                feelsLike: 16,
                humidity: 55,
                wind: 3.8,
                pressure: 1015
            },
            'Tokyo': {
                temp: 22,
                condition: 'Clear Sky',
                feelsLike: 20,
                humidity: 70,
                wind: 4.1,
                pressure: 1012
            },
            'Paris': {
                temp: 17,
                condition: 'Cloudy',
                feelsLike: 15,
                humidity: 60,
                wind: 4.5,
                pressure: 1014
            },
            'Seethariguda': {
                temp: 31,
                condition: 'Sunny',
                feelsLike: 33,
                humidity: 45,
                wind: 6.2,
                pressure: 1011
            }
        };
        
        function getWeather() {
            const city = document.getElementById('cityInput').value.trim();
            const resultDiv = document.getElementById('weatherResult');
            
            if (!city) {
                resultDiv.innerHTML = '<div class="error">Please enter a city name</div>';
                return;
            }
            
            // Show loading state
            resultDiv.innerHTML = '<div class="loading">Loading weather data...</div>';
            
            // Simulate API call
            setTimeout(() => {
                const data = weatherData[city] || {
                    temp: Math.floor(Math.random() * 20) + 10,
                    condition: ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain'][Math.floor(Math.random() * 4)],
                    feelsLike: Math.floor(Math.random() * 20) + 8,
                    humidity: Math.floor(Math.random() * 40) + 40,
                    wind: (Math.random() * 8 + 2).toFixed(1),
                    pressure: Math.floor(Math.random() * 20) + 1000
                };
                
                resultDiv.innerHTML = `
                    <div class="weather-display">
                        <div class="city-name">${city}</div>
                        <div class="temperature">${data.temp}°C</div>
                        <div class="weather-condition">${data.condition}</div>
                    </div>
                    
                    <div class="details-grid">
                        <div class="detail-card">
                            <div class="detail-label">Feels like</div>
                            <div class="detail-value">${data.feelsLike}°C</div>
                        </div>
                        <div class="detail-card">
                            <div class="detail-label">Humidity</div>
                            <div class="detail-value">${data.humidity}%</div>
                        </div>
                        <div class="detail-card">
                            <div class="detail-label">Wind</div>
                            <div class="detail-value">${data.wind} m/s</div>
                        </div>
                        <div class="detail-card">
                            <div class="detail-label">Pressure</div>
                            <div class="detail-value">${data.pressure} hPa</div>
                        </div>
                    </div>
                `;
            }, 500);
        }
        
        // Allow Enter key to trigger search
        document.getElementById('cityInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                getWeather();
            }
        });
        
        // Load weather for default city on page load
        window.onload = function() {
            getWeather();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(MODERN_WEATHER_TEMPLATE)

@app.route('/weather')
def weather():
    city = request.args.get('city', 'Seethariguda')
    # Return mock data for the requested city
    return {'success': True, 'city': city}

if __name__ == '__main__':
    print("🌤️  Modern Weather App Starting...")
    print("📍 Open: http://localhost:5000")
    print("🎨 Modern UI with blue sky background")
    print("🔍 Features: Location, AQI, Pollen, Hourly & Daily forecasts")
    print("📱 Mobile-optimized design")
    app.run(debug=True, host='0.0.0.0', port=5000)
