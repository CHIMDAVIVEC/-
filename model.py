from wtforms import Form, FloatField, IntegerField, StringField, validators
from math import pi
import functools

def check_interval(form, field, min_value=None, max_value=None):
    """For validation: failure if value is outside an interval."""
    failure = False
    if min_value is not None:
        if field.data < min_value:
            failure = True
    if max_value is not None:
        if field.data > max_value:
            failure = True
    if failure:
        raise validators.ValidationError(
            '%s=%s not in [%s, %s]' %
            (field.name, field.data,
             '-infty' if min_value is None else str(min_value),
             'infty'  if max_value is None else str(max_value)))

def interval(min_value=None, max_value=None):
    """Flask-compatible interface to check_interval."""
    return functools.partial(
        check_interval, min_value=min_value, max_value=max_value)

class Isolines(Form):
    Z = FloatField(
        label='Количество изолиний', default=5.0,
        validators=[validators.InputRequired(), interval(5,20)])
####
#Технические параметры
class TechParams(Form):
    K = FloatField(
        label='Коэффициент обрабатываемости', default=1.0,
        validators=[validators.InputRequired(), interval(0.1,1)])

    d = FloatField(
        label='Диаметр сверла [мм]', default=4.2,
        validators=[validators.InputRequired(), interval(0,None)])
####
#Экономические параметры
class EconomicParams(Form):
    t_z = FloatField(
        label='Время на заточку инструмента [Мин]', default=2.5,
        validators=[validators.InputRequired(), interval(0,None)])

    k_s = FloatField(
        label='Количество переточек до полного износа', default=10,
        validators=[validators.InputRequired(), interval(1,None)])

    L0 = FloatField(
        label='Длина отверстия [мм]', default=838.0,
        validators=[validators.InputRequired(), interval(0,None)])

    LC = FloatField(
        label='Количество отверстий в изделии', default=20,
        validators=[validators.InputRequired(), interval(0,None)])

    t_u = FloatField(
        label='Время на смену инструмента [Мин]', default=3.0,
        validators=[validators.InputRequired(), interval(0,None)])

    c_p = FloatField(
        label='Покупная стоимость инструмента [Руб]', default=50.0,
        validators=[validators.InputRequired(), interval(0,None)])

    c_u = FloatField(
        label='Зарплата сверловщика [Руб/Мес]', default=18181.7,
        validators=[validators.InputRequired(), interval(0,None)])

    c_z = FloatField(
        label='Зарплата заточника [Руб/Мес]', default=18181.7,
        validators=[validators.InputRequired(), interval(0,None)])
####
#Параметры учета электроэнергии
class ElectroParams(Form):
    N_o = FloatField(
        label='Мощность основного оборудования [кВт]', default=15.0,
        validators=[validators.InputRequired(), interval(0,None)])

    N_z = FloatField(
        label='Мощность заточного оборудования [кВт]', default=2.2,
        validators=[validators.InputRequired(), interval(0,None)])

    N_p = FloatField(
        label='Тариф на электроэнергию [Руб/кВт*ч]', default=2.0,
        validators=[validators.InputRequired(), interval(0,None)])
####
#Вывод при оптимальном режиме
class Optimal(Form):
    n = IntegerField(label='Частота вращения n [об/мин]')
    So = IntegerField(label='Подача на оборот So [мм/об]')
    V = IntegerField(label='Скорость резания V [мм/Мин]')
    Sm = IntegerField(label='Минутная подача Sm [мм/Мин]')
    L = IntegerField(label='Стойкость L [мм]')
    T = IntegerField(label='Стойкость T [Мин]')
    Q = IntegerField(label='Экономический критерий Q [Руб/Дет]')
#Вывод при режиме макс. стойкости
class Max(Form):
    n = IntegerField(label='Частота вращения n [об/мин]')
    So = IntegerField(label='Подача на оборот So [мм/об]')
    V = IntegerField(label='Скорость резания V [мм/Мин]')
    Sm = IntegerField(label='Минутная подача Sm [мм/Мин]')
    L = IntegerField(label='Стойкость L [мм]')
    T = IntegerField(label='Стойкость T [Мин]')
    Q = IntegerField(label='Экономический критерий Q [Руб/Дет]')