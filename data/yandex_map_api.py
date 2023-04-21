import requests


def get_location_map(location):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    delta = "0.1"
    map_params = {
        "ll": ",".join([str(location[0]), str(-location[1])]),  # координаты центра карты
        "spn": ",".join([delta, delta]),  # размер области карты
        "l": "map",  # тип карты
        "pt": ",".join([str(location[0]), str(-location[1]), "pm2rdl"]),  # ставим метку на карту
        "size": "650,450"
    }
    # print(map_params)
    response = requests.get(map_api_server, params=map_params)
    map_file = f"static\img\{map_params['ll'].replace(',', '-').replace('.', '_')}.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file
