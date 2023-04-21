#!/usr/bin/python3
import os
import datetime
from geolite2 import geolite2
from pprint import pprint
from flask import Flask, render_template, redirect, request, session
from data.sky_map import get_astronet_sky_map  # получение карты звездного неба с сайта www.astronet.ru
from data.yandex_map_api import get_location_map  # получение карты местоположения наблюдателя
from forms.sky_params import SkyForm
import logging

# Настраиваем логгирование
logging.basicConfig(filename='sky.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')

# создаем приложение
app = Flask(__name__)

# защита от межсайтовой подделки запросов https://ru.wikipedia.org/wiki/Межсайтовая_подделка_запроса
app.config['SECRET_KEY'] = '9CAlTN8jKiQg'

geo_reader = geolite2.reader()

# обработчик обращения к страницам "http://<сайт>/" и "http://<сайт>/index"
@app.route('/')
@app.route('/index')
def index():
    ip_addr = request.remote_addr
    if not session:
        ip_location = geo_reader.get(ip_addr)
        if ip_location:
            latitude = ip_location['location']['latitude']
            longitude = ip_location['location']['longitude']
            print(f'by ip latitude = {latitude} longitude = {longitude}')
        else:
            latitude = 46.307743
            longitude = 44.269759
            print(f'by default(Элиста) latitude = {latitude} longitude = {longitude}')

        session['m'] = 5.0
        session['latitude'] = longitude
        session['longitude'] = -latitude
        session['azimuth'] = 0
        session['xs'] = '1024'
        session['dgrids'] = 1
        session['dcbnd'] = 0
        session['dfig'] = 1
        session['colstars'] = 1
        session['names'] = 1
        session['dpl'] = 1
        session['drawmw'] = 1

    # print(session)
    location = (session['latitude'], session['longitude'], session['azimuth'])
    # print(get_location_map(location))
    # print(location)
    dt = datetime.datetime.utcnow()
    t = dt.time()
    ut = t.hour + t.minute / 60 + t.second / 3600
    query_params = {
        'ut': f"{ut:0.5}",
        'day': dt.day,
        'month': dt.month,
        'year': dt.year,

        # Элиста
        # 'longitude': -46.307743,
        # 'latitude': 44.269759,
        'longitude': session['longitude'],
        'latitude': session['latitude'],
        'azimuth': session.get('azimuth', 180),

        'height': 0,
        'm': session['m'],  # звездные величины
        'dgrids': session['dgrids'],
        'dcbnd': session['dcbnd'],  # границы созвездий
        'dfig': session['dfig'],  # фигуры созвездий
        'colstars': session['colstars'],  # отображение спектральных классов
        'names': session['names'],
        'xs': session.get('xs', 1024),  # размер картинки
        'theme': 0,
        'dpl': session['dpl'],  # планеты
        'drawmw': session['drawmw'],
        'pdf': 0,
        'lang': 1  # язык
    }
    with open("static/img/skyc.gif", "wb") as sky:
        sky.write(get_astronet_sky_map(query_params))
    return render_template('index.html', title='Звездная карта', ip=ip_addr, location=location, map=get_location_map(location))


# обработчик формы установки параметров карты
@app.route('/sky_params',  methods=['GET', 'POST'])
# @login_required
def sky_params():
    form = SkyForm()

    if form.validate_on_submit():

        session['latitude'] = form.latitude.data
        session['longitude'] = form.longitude.data
        session['azimuth'] = form.azimuth.data
        session['xs'] = form.xs.data
        session['m'] = form.m.data

        session['dgrids'] = int(form.dgrids.data)
        session['colstars'] = int(form.colstars.data)
        session['dcbnd'] = int(form.dcbnd.data)
        session['dfig'] = int(form.dfig.data)
        session['dpl'] = int(form.dpl.data)
        session['names'] = int(form.names.data)
        session['drawmw'] = int(form.drawmw.data)

        # pprint(session)

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
        session['latitude'] = params['latitude']
        session['longitude'] = params['longitude']

        params['azimuth'] = form.azimuth.data
        session['azimuth'] = params['azimuth']
        params['height'] = 0
        # params['m'] = 5.0
        params['m'] = form.m.data
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
        # pprint(params)

        with open("static/img/skyc.gif", "wb") as sky:
            sky.write(get_astronet_sky_map(params))

        location = (session['latitude'], session['longitude'], session['azimuth'])
        return render_template('index.html', title='Звездная карта', ip=request.remote_addr, location=location, map=get_location_map(location))
    else:
        if session:
            form.latitude.data = session.get('latitude', 44.269759)
            form.longitude.data = session.get('longitude', -46.307743)
            form.azimuth.data = session.get('azimuth', '0')
            form.xs.data = session.get('xs', '1024')
            form.dgrids.data = session['dgrids']
            form.colstars.data = session['colstars']
            form.dcbnd.data = session['dcbnd']
            form.dfig.data = session['dfig']
            form.dpl.data = session['dpl']
            form.names.data = session['names']
            form.drawmw.data = session['drawmw']
            form.m.data = session['m']

    location = (session['latitude'], session['longitude'], session['azimuth'])
    # print(f'sky_params {location}')
    return render_template('sky_params.html', title='Параметры карты', ip=request.remote_addr, location=location,
                           form=form)


# запуск приложения app "слушаем" на всех адресах и на порту 5000 (наружу настроен проброс с порта 54321)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
