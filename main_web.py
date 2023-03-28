import os
import datetime
from flask import Flask, render_template
from data.sky_map import get_astronet_sky_map

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    dt = datetime.datetime.utcnow()
    t = dt.time()
    ut = t.hour + t.minute / 60 + t.second / 3600
    query_params = {
        'ut': f"{ut:0.5}",
        'day': dt.day,
        'month': dt.month,
        'year': dt.year,

        'longitude': -46.307743,
        'latitude': 44.269759,
        'azimuth': 180,

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
    with open("static/img/skyc.gif", "wb") as sky:
        sky.write(get_astronet_sky_map(query_params))
    return render_template('index.html', title='Звездная карта')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
