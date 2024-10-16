from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

# 过滤器
@app.template_filter()
def format_speed_wind(value):
    speed_wind_data = {
        1: "Below 0.3m/s (calm)",
        2: "0.3-3.4m/s (light)",
        3: "3.4-8.0m/s (moderate)",
        4: "8.0-10.8m/s (fresh)",
        5: "10.8-17.2m/s (strong)",
        6: "17.2-24.5m/s (gale)",
        7: "24.5-32.6m/s (storm)",
        8: "Over 32.6m/s (hurricane)",
    }
    return speed_wind_data.get(value)

@app.template_filter()
def format_weather( value):
    mappings = {
        'cloudy': 'Cloudy',
        'ts': 'Thunderstorm',
        'lightrain': 'Light Rain'
    }
    return mappings.get(value, value.capitalize())

def get_latitude_longitude_baidu(city):
    url = "https://api.map.baidu.com/geocoding/v3"
    ak = 'nRiOFdz02tlNqCmQnOYtN9xsSqxRvmcU'
    params = {
        "address": city,
        "output": "json",
        "ak": ak,
    }
    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['status'] == 0:
            location = result['result']['location']
            return location['lat'], location['lng']
    return None, None

def get_weather_data(city):
    # open api url: https://www.7timer.info/doc.php?lang=en
    lon, lat = get_latitude_longitude_baidu(city)
    # lon, lat = 113.17, 23.09
    req_url = f"https://www.7timer.info/bin/civillight.php?lon={lon}&lat={lat}&ac=0&lang=en&unit=metric&output=json&tzshift=0"
    response = requests.get(req_url)
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            try:
                response = get_weather_data(city)
                weather_data = response.json()
            except Exception as e:
                error = str(e)
        else:
            error = 'Please enter a city name.'
    
    return render_template('index.html', weather_data=weather_data, error=error)

if __name__ == '__main__':
    # https可在nginx中配置
    app.run(debug=True)