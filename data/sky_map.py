import requests


# функция загрузки карты с сайта www.astronet.ru
def get_astronet_sky_map(params):
    api_server = "http://www.astronet.ru/cgi-bin/skyc.cgi"
    response = requests.get(api_server, params=params)
    return response.content
