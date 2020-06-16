import pyowm
import datetime as dt
import os

# Current weather, minute forecast for 1 hour, hourly forecast for 48 hours,
# daily forecast for 7 days, historical data for 5 previous days for any location
# https://github.com/csparpa/pyowm
# https://pyowm.readthedocs.io/en/latest/usage-examples-v2/weather-api-usage-examples.html#owm-weather-api-version-2-5-usage-examples


def weather(place='Novosibirsk'):
    try:
        owm = pyowm.OWM(os.environ['API_KEY_WEATHER'], language='ru')

        # Search for current weather in place
        observation = owm.weather_at_place(place)
        w = observation.get_weather()

    except Exception as e:
        print(repr(e))
        return None

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


def forecast_weather(place_fc='Novosibirsk'):
    # forecast
    try:
        owm = pyowm.OWM(os.environ['API_KEY_WEATHER'], language='ru')
        # Query for 3 hours weather forecast for the next 5 days
        fc_3h = owm.three_hours_forecast(place_fc)

    except Exception as e:
        print(repr(e))
        return None

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
        return_dict['time'].append(ref_time)  # Время в Нск относительно  UTC
        return_dict['temperature'].append(weather_.get_temperature('celsius')['temp'])
        return_dict['wind'].append(weather_.get_wind()['speed'])
        return_dict['pressure'].append(int(weather_.get_pressure()['press'] / 1.33322))
        return_dict['detailed_status'].append(weather_.get_detailed_status())

    # When in time does the forecast begin?
    fc_3h.when_starts('date')  # datetime.datetime instance
    # ...and when will it end?
    fc_3h.when_ends('date')  # datetime.datetime instance

    return return_dict


# Возвращает четыре значения для каждого дня: ночь, утро, день, вечер
def forecast_weather_sparse_dict(place_sp='Novosibirsk'):
    weather_dict = forecast_weather(place_sp)

    if weather_dict is None:
        return None

    return_dict_sparse = {'day': [],
                          'month': [],
                          'day_time': [],
                          'temperature': [],
                          'wind': [],
                          'detailed_status': []}
    for i in range(len(weather_dict['time'])):
        if weather_dict['time'][i].hour == 4 or weather_dict['time'][i].hour == 7 or \
                weather_dict['time'][i].hour == 13 or weather_dict['time'][i].hour == 22:
            return_dict_sparse['day'].append(weather_dict['time'][i].day)
            return_dict_sparse['month'].append(weather_dict['time'][i].month)
            return_dict_sparse['temperature'].append(weather_dict['temperature'][i])
            return_dict_sparse['wind'].append(weather_dict['wind'][i])
            return_dict_sparse['detailed_status'].append(weather_dict['detailed_status'][i])

        if weather_dict['time'][i].hour == 4:
            return_dict_sparse['day_time'].append("Ночь")
        elif weather_dict['time'][i].hour == 7:
            return_dict_sparse['day_time'].append("Утро")
        elif weather_dict['time'][i].hour == 13:
            return_dict_sparse['day_time'].append("День")
        elif weather_dict['time'][i].hour == 22:
            return_dict_sparse['day_time'].append("Вечер")
    return return_dict_sparse


# Возвращает список значение для вывода
def forecast_weather_sparse_list(place_ls='Novosibirsk'):
    sparse_dict = forecast_weather_sparse_dict(place_ls)
    # if sparse_dict is None:
    #     return None

    ret_list = []
    for count in range(0, len(sparse_dict["day"]) - 1, 4):
        ret_list.append("{0}-{1}\n{2} t:{3} {4}\n{5} t:{6} {7}\n{8} t:{9} {10}\n{11} t:{12} {13}\n".format(
            str(sparse_dict["day"][count]),
            str(sparse_dict["month"][count]),
            sparse_dict["day_time"][count],
            str(int(sparse_dict["temperature"][count])),
            sparse_dict["detailed_status"][count],
            sparse_dict["day_time"][count + 1],
            str(int(sparse_dict["temperature"][count + 1])),
            sparse_dict["detailed_status"][count + 1],
            sparse_dict["day_time"][count + 2],
            str(int(sparse_dict["temperature"][count + 2])),
            sparse_dict["detailed_status"][count + 2],
            sparse_dict["day_time"][count + 3],
            str(int(sparse_dict["temperature"][count + 3])),
            sparse_dict["detailed_status"][count + 3]))

    return ret_list


if __name__ == '__main__':
    place = "Novosibirsk"
    # weath_dict = weather(place)
    # str1 = "Температура: {0} C\nВлажность: {1}%\n".format(str(weath_dict['temperature']), str(weath_dict['humidity']))
    # print(str1)
    rt_lst = forecast_weather_sparse_list(place)

    print(rt_lst[0])
    # print(rt_lst[1])
    # print(rt_lst[2])
    # print(rt_lst[3])
    # print(rt_lst[4])

