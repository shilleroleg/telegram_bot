import requests
import json
import datetime
import config
"""
Загрузка курсов валют с сайта https://openexchangerates.org
На бесплатном тарифе загружает только относительно USD.

"""


def get_usd_eur():
	http_req_str = 'https://openexchangerates.org/api/latest.json?app_id='

	# Запрос
	response = requests.get(http_req_str + config.EXCHANGE_APP_ID)
	# Получаем JSON
	answer_json = response.json()
	# Выделяем список валют
	answer_rates = answer_json['rates']
	# Интересующие пары валют
	usd_rub = answer_rates['RUB']
	eur_rub = round(usd_rub / answer_rates['EUR'], 2)

	# Время в Unix Timestamp
	timestamp_unix = answer_json['timestamp']
	# Преобразуем в формат 2020-05-10 23:00:05
	time = datetime.datetime.fromtimestamp(timestamp_unix) + datetime.timedelta(hours=7)

	return_dict = {'time': time, 'usd': usd_rub, 'eur': eur_rub}

	return return_dict


def get_list_currencies():
	http_req_str = 'https://openexchangerates.org/api/currencies.json'
	# Запрос
	response = requests.get(http_req_str)
	# Возвращаем JSON
	return response.json()


if __name__ == '__main__':
	ret_dict = get_usd_eur()
	print(ret_dict['time'], ret_dict['usd'], ret_dict['eur'])
