from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField, IntegerField
from flask import session
from wtforms.validators import DataRequired


# класс формы для задания параметров карты
class SkyForm(FlaskForm):

    xs = SelectField('размер картинки', choices=[(512, '512'),
                                                 (640, '640'),
                                                 (800, '800'),
                                                 (1024, '1024'),
                                                 (1152, '1152'),
                                                 (1280, '1280'),
                                                 (1600, '1600')
                                                 ], default=1024)
    theme = IntegerField('тема', default=0)
    m = FloatField('Звездные величины', default=5.0)
    longitude = FloatField('долгота', default=-46.307743)
    latitude = FloatField('широта', default=44.269759)
    # longitude = FloatField('долгота', default=-session['latitude'])
    # latitude = FloatField('широта', default=session['longitude'])
    azimuth = SelectField('направление', choices=[(0, 'Юг'), (90, 'Запад'), (180, 'Север'), (270, 'Восток')], default=180)
    dgrids = BooleanField('разметка', default=True)
    dcbnd = BooleanField('границы созвездий', default=False)
    dfig = BooleanField('фигуры созвездий', default=True)
    colstars = BooleanField('отображение спектральных классов', default=True)
    names = BooleanField('наименования созвездий', default=True)
    dpl = BooleanField('планеты', default=True)
    drawmw = BooleanField('туманности?', default=True)

    submit = SubmitField('Показать')