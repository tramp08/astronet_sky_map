from pprint import pprint
import requests
from PIL import Image
from io import BytesIO
import datetime


dt = datetime.datetime.utcnow()
t = dt.time()
ut = t.hour + t.minute / 60 + t.second / 3600
api_server = "http://www.astronet.ru/cgi-bin/skyc.cgi"
query_params = {
    'ut': f"{ut:0.5}",
    'day': dt.day,
    'month': dt.month,
    'year': dt.year,

    'longitude': -46.307743,
    'latitude': 44.269759,
    'azimuth': 90,

    'height': 0,
    'm': 5.0,  # звездные величины
    'dgrids': 1,
    'dcbnd': 0,  # границы созвездий
    'dfig': 1,  # фигуры созвездий
    'colstars': 1,  # отображение спектральных классов
    'names': 1,
    'xs': 1600,  # размер картинки
    'theme': 0,
    'dpl': 1,  # планеты
    'drawmw': 1,
    'pdf': 0,
    'lang': 1  # язык
}

pprint(query_params)
response = requests.get(api_server, params=query_params)
print(dt)
pprint(response.headers)
print(response.url)
Image.open(BytesIO(
    response.content)).show()