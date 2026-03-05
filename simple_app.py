from flask import Flask, render_template_string, request

app = Flask(__name__)

# Simple HTML template without external dependencies
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Forecast - Simple Version</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 90%;
            text-align: center;
            color: white;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .search-box {
            margin: 30px 0;
            display: flex;
            gap: 10px;
            justify-content: center;
        }
        
        input {
            padding: 12px 20px;
            border: none;
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            font-size: 16px;
            width: 250px;
        }
        
        input::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        
        button {
            padding: 12px 25px;
            border: none;
            border-radius: 25px;
            background: white;
            color: #667eea;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: scale(1.05);
        }
        
        .weather-info {
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
        }
        
        .temp {
            font-size: 3em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .description {
            font-size: 1.2em;
            margin: 10px 0;
            text-transform: capitalize;
        }
        
        .details {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        
        .detail-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 10px;
        }
        
        .error {
            color: #ff6b6b;
            background: rgba(255, 107, 107, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .loading {
            color: #ffd93d;
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ Weather Forecast</h1>
        <p>Beautiful weather app with stunning UI</p>
        
        <div class="search-box">
            <input type="text" id="cityInput" placeholder="Enter city name..." />
            <button onclick="getWeather()">Get Weather</button>
        </div>
        
        <div id="result"></div>
    </div>

    <script>
        async function getWeather() {
            const city = document.getElementById('cityInput').value.trim();
            const resultDiv = document.getElementById('result');
            
            if (!city) {
                resultDiv.innerHTML = '<div class="error">Please enter a city name</div>';
                return;
            }
            
            resultDiv.innerHTML = '<div class="loading">Loading weather data...</div>';
            
            try {
                // Using a simple weather API that doesn't require key for demo
                const response = await fetch(`/weather?city=${encodeURIComponent(city)}`);
                const data = await response.json();
                
                if (data.success) {
                    resultDiv.innerHTML = `
                        <div class="weather-info">
                            <h2>${data.city}</h2>
                            <div class="temp">${data.temperature}°C</div>
                            <div class="description">${data.description}</div>
                            <div class="details">
                                <div class="detail-item">
                                    <strong>Feels like:</strong> ${data.feels_like}°C
                                </div>
                                <div class="detail-item">
                                    <strong>Humidity:</strong> ${data.humidity}%
                                </div>
                                <div class="detail-item">
                                    <strong>Wind:</strong> ${data.wind_speed} m/s
                                </div>
                                <div class="detail-item">
                                    <strong>Pressure:</strong> ${data.pressure} hPa
                                </div>
                            </div>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<div class="error">${data.error}</div>`;
                }
            } catch (error) {
                resultDiv.innerHTML = '<div class="error">Failed to fetch weather data</div>';
            }
        }
        
        // Allow Enter key to trigger search
        document.getElementById('cityInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                getWeather();
            }
        });
        
        // Load weather for default city on page load
        window.onload = function() {
            document.getElementById('cityInput').value = 'London';
            getWeather();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/weather')
def weather():
    city = request.args.get('city')
    if not city:
        return {'success': False, 'error': 'City parameter required'}
    
    # Simple mock weather data for demonstration
    mock_data = {
        'London': {'temp': 15, 'desc': 'partly cloudy', 'humidity': 65, 'wind': 5.2, 'pressure': 1013},
        'New York': {'temp': 18, 'desc': 'sunny', 'humidity': 55, 'wind': 3.8, 'pressure': 1015},
        'Tokyo': {'temp': 22, 'desc': 'clear sky', 'humidity': 70, 'wind': 4.1, 'pressure': 1012},
        'Paris': {'temp': 17, 'desc': 'cloudy', 'humidity': 60, 'wind': 4.5, 'pressure': 1014},
        'Sydney': {'temp': 25, 'desc': 'sunny', 'humidity': 50, 'wind': 6.2, 'pressure': 1011}
    }
    
    if city in mock_data:
        data = mock_data[city]
        return {
            'success': True,
            'city': city,
            'temperature': data['temp'],
            'description': data['desc'],
            'feels_like': data['temp'] - 2,
            'humidity': data['humidity'],
            'wind_speed': data['wind'],
            'pressure': data['pressure']
        }
    else:
        # Generate random weather data for unknown cities
        import random
        return {
            'success': True,
            'city': city,
            'temperature': random.randint(10, 30),
            'description': random.choice(['sunny', 'partly cloudy', 'cloudy', 'light rain']),
            'feels_like': random.randint(8, 32),
            'humidity': random.randint(40, 80),
            'wind_speed': round(random.uniform(2, 10), 1),
            'pressure': random.randint(1000, 1020)
        }

if __name__ == '__main__':
    print("🌤️  Starting Simple Weather App...")
    print("📍 Open http://localhost:5000 in your browser")
    print("🎨 Beautiful UI with glass morphism effect")
    print("🔍 Try cities: London, New York, Tokyo, Paris, Sydney")
    app.run(debug=True, host='0.0.0.0', port=5000)
