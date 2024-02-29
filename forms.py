from wtforms import Form
from flask_wtf import FlaskForm

from wtforms import Form, StringField, IntegerField, validators, FloatField


class UserForm2(Form):
    id=IntegerField('id',
                    [validators.number_range(min=1, max=20, message='valor no valido')])
    
    nombre = StringField('nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=30, message='Ingresa un nombre válido')
    ])

    direcccion = StringField('direcccion', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa un apellido válido')
    ])
    
    telefono = StringField('telefono', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=10, message='Ingresa un apellido válido')
    ])

    email = StringField('email', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Email(message='Ingresa un email válido')
    ])

    sueldo = FloatField('sueldo', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa un apellido válido')
    ])