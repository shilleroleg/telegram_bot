import pyowm
import config

# Current weather, minute forecast for 1 hour, hourly forecast for 48 hours,
# daily forecast for 7 days, historical data for 5 previous days for any location
# https://github.com/csparpa/pyowm
# https://pyowm.readthedocs.io/en/latest/usage-examples-v2/weather-api-usage-examples.html#owm-weather-api-version-2-5-usage-examples


def weather(place='Novosibirsk'):
    owm = pyowm.OWM(config.API_KEY_WEATHER, language='ru')

    # Search for current weather in place
    observation = owm.weather_at_place(place)
    w = observation.get_weather()

    # Observation objects also contain a Location object with info about the weather location:
    location = observation.get_location()
    lon = location.get_lon()
    lat = location.get_lat()
    loc_id = location.get_ID()
    print(lon, lat)

    # Weather details
    time = w.get_reference_time(timeformat='date')  # get time of observation as a datetime.datetime object

    wind = w.get_wind()  # {'speed': 4.6, 'deg': 330}
    humidity = w.get_humidity()  # 87
    temper = w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

    # print(f"time: {time}\nwind: {wind} \nhumidity: {humidity}\ntemperature: {temper}")

    clouds = w.get_clouds()  # Get cloud coverage 65
    rain = w.get_rain()  # Get rain volume {'3h': 0}
    snow = w.get_snow()  # Get snow volume {}
    pressure = w.get_pressure()  # Get atmospheric pressure {'press': 1009, 'sea_level': 1038.381}
    status = w.get_status()  # Get weather short status 'clouds'
    det_status = w.get_detailed_status()  # Get detailed weather status 'Broken clouds'
    sunrise = w.get_sunrise_time('iso')  # Sunrise time (GMT UNIXtime or ISO 8601) 1377862896L
    sunset = w.get_sunset_time('iso')  # Sunset time (GMT UNIXtime or ISO 8601) '2013-08-30 20:07:57+00'

    return_dict = {'time': time,
                   'temperature': temper['temp'],
                   'humidity': humidity,
                   'wind': wind['speed'],
                   'pressure': pressure['press'],
                   'detailed_status': det_status,
                   'cloud': clouds,
                   'sunrise': sunrise,
                   'sunset': sunset}

    # print(clouds, rain, snow, pressure, det_status, sunrise, sunset)

    # The query returns an UV Index value entity instance
    # https://en.wikipedia.org/wiki/Ultraviolet_index
    uvi = owm.uvindex_around_coords(lat, lon)

    uv_val = uvi.get_value()
    uv_risk = uvi.get_exposure_risk()  # methods returns a string estimating the risk of harm from unprotected sun exposure if an average adult was exposed to a UV intensity such as the on in this measurement.
    # print(uv_val, uv_risk)
    return_dict['uv_val'] = uv_val
    return_dict['uv_risk'] = uv_risk

    return return_dict


def forecast(place='Novosibirsk'):
    # forecast
    owm = pyowm.OWM(config.API_KEY_WEATHER, language='ru')
    # Query for 3 hours weather forecast for the next 5 days
    fc_3h = owm.three_hours_forecast(place)

    forecast_3h = fc_3h.get_forecast()

    # Get the list of Weather objects...
    # lst = forecast_3h.get_weathers()
    # ...or iterate directly over the Forecast object
    for weather in forecast_3h:
        # print (weather.get_reference_time('iso'), weather.get_temperature('celsius'))
        pass

    # When in time does the forecast begin?
    fc_3h.when_starts('date')  # datetime.datetime instance
    # ...and when will it end?
    fc_3h.when_ends('date')  # datetime.datetime instance

    return forecast_3h


if __name__ == '__main__':
    weather("Сургут")
