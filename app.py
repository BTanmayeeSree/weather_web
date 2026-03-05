from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from dotenv import load_dotenv
import json
from datetime import datetime
import pytz

load_dotenv()

app = Flask(__name__)
CORS(app)

# OpenWeatherMap API configuration
API_KEY = os.getenv('WEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5"
GEO_URL = "http://api.openweathermap.org/geo/1.0"

# Initialize geocoder
geolocator = Nominatim(user_agent="weather_app")

def get_location_by_ip():
    """Get user location by IP address"""
    try:
        response = requests.get(f'http://ip-api.com/json/')
        if response.status_code == 200:
            data = response.json()
            return {
                'lat': data['lat'],
                'lon': data['lon'],
                'city': data['city'],
                'country': data['country']
            }
    except:
        pass
    return None

def get_location_by_name(city_name):
    """Get coordinates for a city name"""
    try:
        location = geolocator.geocode(city_name)
        if location:
            return {
                'lat': location.latitude,
                'lon': location.longitude,
                'city': location.address.split(',')[0],
                'full_address': location.address
            }
    except (GeocoderTimedOut, GeocoderServiceError):
        pass
    return None

def get_weather_data(lat, lon):
    """Get comprehensive weather data"""
    try:
        # Current weather
        current_url = f"{BASE_URL}/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY,
            'units': 'metric'
        }
        current_response = requests.get(current_url, params=params)
        current_data = current_response.json()

        # 5-day forecast
        forecast_url = f"{BASE_URL}/forecast"
        forecast_response = requests.get(forecast_url, params=params)
        forecast_data = forecast_response.json()

        # Air pollution
        pollution_url = f"{BASE_URL}/air_pollution"
        pollution_params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY
        }
        pollution_response = requests.get(pollution_url, params=pollution_params)
        pollution_data = pollution_response.json()

        return {
            'current': current_data,
            'forecast': forecast_data,
            'pollution': pollution_data,
            'success': True
        }
    except Exception as e:
        return {'error': str(e), 'success': False}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather')
def get_weather():
    # Try to get location from query parameters
    city = request.args.get('city')
    
    if city:
        location = get_location_by_name(city)
    else:
        # Try IP-based location detection
        location = get_location_by_ip()
    
    if not location:
        return jsonify({'error': 'Location not found', 'success': False})
    
    weather_data = get_weather_data(location['lat'], location['lon'])
    
    if weather_data.get('success'):
        weather_data['location'] = location
    
    return jsonify(weather_data)

@app.route('/api/location-search')
def search_location():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'No query provided', 'success': False})
    
    location = get_location_by_name(query)
    if location:
        weather_data = get_weather_data(location['lat'], location['lon'])
        if weather_data.get('success'):
            weather_data['location'] = location
            return jsonify(weather_data)
    
    return jsonify({'error': 'Location not found', 'success': False})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
