#!/usr/bin/python3
import os
import datetime
from pprint import pprint
from flask import Flask, render_template, redirect
from data.sky_map import get_astronet_sky_map
from forms.sky_params import SkyForm
import logging

# Настраиваем логгирование
logging.basicConfig(filename='sky.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')

# создаем приложение
app = Flask(__name__)
# защита от межсайтовой подделки запросов https://ru.wikipedia.org/wiki/Межсайтовая_подделка_запроса
app.config['SECRET_KEY'] = '9CAlTN8jKiQg'


# обработчик обращения к страницам "http://<сайт>/" и "http://<сайт>/index"
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

        # Элиста
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
        'xs': 800,  # размер картинки
        'theme': 0,
        'dpl': 1,  # планеты
        'drawmw': 1,
        'pdf': 0,
        'lang': 1  # язык
    }
    with open("static/img/skyc.gif", "wb") as sky:
        sky.write(get_astronet_sky_map(query_params))
    return render_template('index.html', title='Звездная карта')


# обработчик формы установки параметров карты
@app.route('/sky_params',  methods=['GET', 'POST'])
# @login_required
def add_news():
    form = SkyForm()
    if form.validate_on_submit():
        print(form)

        dt = datetime.datetime.utcnow()
        t = dt.time()
        ut = t.hour + t.minute / 60 + t.second / 3600

        params = {}

        # текущее время
        params['ut'] = f"{ut:0.5}"
        params['day'] = dt.day
        params['month'] = dt.month
        params['year'] = dt.year

        # Элиста
        params['longitude'] = form.longitude.data
        params['latitude'] = form.latitude.data

        params['azimuth'] = form.azimuth.data
        params['height'] = 0
        params['m'] = 5.0
        params['dgrids'] = int(form.dgrids.data)
        params['dcbnd'] = int(form.dcbnd.data)
        params['dfig'] = int(form.dfig.data)
        params['colstars'] = int(form.colstars.data)
        params['names'] = int(form.names.data)
        params['xs'] = form.xs.data
        params['theme'] = int(form.theme.data)
        params['dpl'] = int(form.dpl.data)
        params['drawmw'] = int(form.drawmw.data)
        params['pdf'] = 0
        params['lang'] = 1
        pprint(params)

        with open("static/img/skyc.gif", "wb") as sky:
            sky.write(get_astronet_sky_map(params))

        return render_template('index.html', title='Звездная карта')
    return render_template('sky_params.html', title='Параметры карты',
                           form=form)


# запуск приложения app "слушаем" на всех адресах и на порту 5000 (наружу настроен проброс с порта 54321)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
