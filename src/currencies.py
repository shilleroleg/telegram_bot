import requests
import json
import datetime
import config

"""
Загрузка курсов валют с сайта https://openexchangerates.org
На бесплатном тарифе загружает только относительно USD.

"""


def get_currencies_pair():
    http_req_str = 'https://openexchangerates.org/api/latest.json?app_id='

    # Запрос
    response = requests.get(http_req_str + config.EXCHANGE_APP_ID)
    # Получаем JSON
    answer_json = response.json()
    # Выделяем список валют
    answer_rates = answer_json['rates']
    # Интересующие пары валют
    usd_rub = round(answer_rates['RUB'], 2)
    eur_rub = round(usd_rub / answer_rates['EUR'], 2)
    cny_rub = round(usd_rub / answer_rates['CNY'], 2)  # Chinese Yuan
    gbp_rub = round(usd_rub / answer_rates['GBP'], 2)  # British Pound Sterling
    uah_rub = round(usd_rub / answer_rates['UAH'], 2)  # Ukrainian Hryvnia
    byn_rub = round(usd_rub / answer_rates['BYN'], 2)  # Belarusian Ruble
    btc_rub = round(usd_rub / answer_rates['BTC'] / usd_rub, 1)  # Bitcoin in $

    # Время в Unix Timestamp
    timestamp_unix = answer_json['timestamp']
    # Преобразуем в формат 2020-05-10 23:00:05
    time = datetime.datetime.fromtimestamp(timestamp_unix) + datetime.timedelta(hours=7)

    return_dict = {'time': time, 'usd': usd_rub, 'eur': eur_rub, 'cny': cny_rub, 'gbp': gbp_rub,
                   'uah': uah_rub, 'byn': byn_rub, 'btc': btc_rub}

    return return_dict


def get_list_currencies():
    http_req_str = 'https://openexchangerates.org/api/currencies.json'
    # Запрос
    response = requests.get(http_req_str)
    # Возвращаем JSON
    return response.json()


if __name__ == '__main__':
    ret_dict = get_currencies_pair()
    print(ret_dict['time'], ret_dict['usd'], ret_dict['eur'])
    print(ret_dict['cny'], ret_dict['gbp'], ret_dict['uah'])
    print(ret_dict['byn'], ret_dict['btc'])
