from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        # You could render "City Not Found" instead like we do below
        city = "Kansas City"

    weather_data = get_current_weather(city)

    # City is not found by API
    if "error" in weather_data:
        return render_template('city-not-found.html')
    #if not weather_data['cod'] == 200:
        #return render_template('city-not-found.html')

    return render_template(
        "weather.html",
        title=weather_data["location"]["name"],
        status=weather_data["current"]["condition"]["text"].capitalize(),
        temp=f"{weather_data['current']['temp_f']:.1f}",
        feels_like=f"{weather_data['current']['feelslike_f']:.1f}"
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
