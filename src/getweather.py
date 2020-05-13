import pyowm
import datetime as dt
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

    # Weather details
    time = w.get_reference_time(timeformat='date')  # get time of observation as a datetime.datetime object in UTC
    time += dt.timedelta(hours=7)   # Время в Нск относительно  UTC

    wind = w.get_wind()  # {'speed': 4.6, 'deg': 330}
    humidity = w.get_humidity()  # 87
    temper = w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

    clouds = w.get_clouds()  # Get cloud coverage 65
    rain = w.get_rain()  # Get rain volume {'3h': 0}
    snow = w.get_snow()  # Get snow volume {}
    pressure = w.get_pressure()  # Get pressure {'press': 1009, 'sea_level': 1038.381} in mm.hg
    status = w.get_status()  # Get weather short status 'clouds'
    det_status = w.get_detailed_status()  # Get detailed weather status 'Broken clouds'
    sunrise = w.get_sunrise_time()  # Sunrise time (GMT UNIXtime or ISO 8601) 1377862896L
    sunrise = dt.datetime.fromtimestamp(sunrise) + dt.timedelta(hours=7)
    sunset = w.get_sunset_time()  # Sunset time (GMT UNIXtime or ISO 8601) '2013-08-30 20:07:57+00'
    # print(type(sunset))
    sunset = dt.datetime.fromtimestamp(sunset) + dt.timedelta(hours=7)

    return_dict = {'time': time,
                   'temperature': temper['temp'],
                   'humidity': humidity,
                   'wind': wind['speed'],
                   'pressure': pressure['press'],
                   'detailed_status': det_status,
                   'cloud': clouds,
                   'sunrise': sunrise,
                   'sunset': sunset}

    # The query returns an UV Index value entity instance
    # https://en.wikipedia.org/wiki/Ultraviolet_index
    uvi = owm.uvindex_around_coords(lat, lon)

    uv_val = uvi.get_value()
    # methods returns a string estimating the risk of harm from unprotected sun exposure
    # if an average adult was exposed to a UV intensity such as the on in this measurement.
    uv_risk = uvi.get_exposure_risk()

    return_dict['uv_val'] = uv_val
    return_dict['uv_risk'] = uv_risk

    return return_dict


def forecast_weather(place='Novosibirsk'):
    # forecast
    owm = pyowm.OWM(config.API_KEY_WEATHER, language='ru')
    # Query for 3 hours weather forecast for the next 5 days
    fc_3h = owm.three_hours_forecast(place)

    forecast_3h = fc_3h.get_forecast()

    # Get the list of Weather objects...
    # lst = forecast_3h.get_weathers()
    # ...or iterate directly over the Forecast object
    return_dict = {'time': [],
                   'temperature': [],
                   'wind': [],
                   'pressure': [],
                   'detailed_status': []}
    for weather_ in forecast_3h:
        ref_time = dt.datetime.fromtimestamp(weather_.get_reference_time())
        return_dict['time'].append(ref_time + dt.timedelta(hours=7))  # Время в Нск относительно  UTC
        return_dict['temperature'].append(weather_.get_temperature('celsius')['temp'])
        return_dict['wind'].append(weather_.get_wind()['speed'])
        return_dict['pressure'].append(int(weather_.get_pressure()['press'] / 1.33322))
        return_dict['detailed_status'].append(weather_.get_detailed_status())

    # When in time does the forecast begin?
    fc_3h.when_starts('date')  # datetime.datetime instance
    # ...and when will it end?
    fc_3h.when_ends('date')  # datetime.datetime instance

    return return_dict


if __name__ == '__main__':
    place = "Novosibirsk"
    weath_dict = weather(place)
    str0 = place + " {0}\n".format(str(weath_dict['time']))

    str1 = "Температура: {0} C\nВлажность: {1}%\n".format(str(weath_dict['temperature']), str(weath_dict['humidity']))
    str2 = "Давление {0} мм.рт.ст\nВетер: {1} м/с\n".format(str(int(weath_dict['pressure'] / 1.33322)),
                                                            str(weath_dict['wind']))
    str3 = "UV-индекс: {0}\nUV-риск: {1}\n".format(str(weath_dict['uv_val']), str(weath_dict['uv_risk']))
    print(str0 + str1 + str2 + str3)
    # forecast_weather("Novosibirsk")