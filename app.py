from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Hardcoded OpenWeatherMap API key
OPENWEATHERMAP_API_KEY = 'd43e17e034bda072a9675280d5ef485f'

def get_location(ip):
    response = requests.get(f'https://ipinfo.io/{ip}/json')
    data = response.json()
    return data.get('city', 'Unknown')

def get_weather(city):
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather', params={
        'q': city,
        'appid': OPENWEATHERMAP_API_KEY,
        'units': 'metric'
    })
    data = response.json()
    return data['main']['temp']

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Hello API! Use the /api/hello endpoint."

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    city = get_location(client_ip)
    temperature = get_weather(city)
    
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
    response_data = {
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)