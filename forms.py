from wtforms import Form
from flask_wtf import FlaskForm

from wtforms import Form, StringField, IntegerField,validators, FloatField,  DateField, RadioField, BooleanField, SelectMultipleField
from datetime import datetime
from wtforms import widgets


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
    
    
    
class UserForm3(Form):
    id = IntegerField('id',
                      [validators.number_range(min=1, max=20, message='valor no valido')])

    nombre = StringField('nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa un nombre válido')#num 30 en max
    ])

    direcccion = StringField('direcccion', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa una direccion válido')
    ])

    telefono = StringField('telefono', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=10, message='Ingresa un telefono válido')
    ])

    tamanopizza = RadioField('Tamaño de Pizza', choices=[
        (40, 'Pequeña'),
        (80, 'Mediana'),
        (120,'Grande')
    ], validators=[validators.DataRequired(message='El campo es requerido')])

    jamon=BooleanField('Jamon', default=False)
    pina=BooleanField('Piña', default=False)
    champinon=BooleanField('Champiñon', default=False)
     
    # ingrediente=[]
    # if jamon == True:
    #   ingrediente.append("Jamon")
    # elif pina == True:
    #   ingrediente.append("Piña")
    # elif champinon == True:
    #   ingrediente.append("Champiñon")
      
    # ingrediente_str = ', '.join(ingrediente) if isinstance(ingrediente, list) else ''

    numpizza = FloatField('numpizza', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=1, max=50, message='Ingresa un numero de pizza válido')
    ])
    
    #fecha_default = datetime.now().strftime('%Y-%m-%d')

# Definir el campo de fecha con el valor predeterminado
    fecha = DateField('fecha', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa una fecha válido')
    ])
    
class busqueda(Form):
    palabra = StringField("Nombre",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")])
    fecha = DateField("Fecha",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")])
    filtro = RadioField('Filtro', choices=[("1", 'Dia'), ("2",'Mes'), ("3",'Año')])
    
    

class Pizza(Form):
    tamanio = RadioField('Tamaño', choices=[('Chica', 'Chica $40'), ('Mediana','Mediana $80'), ('Grande','Grande $120')])
    ingredientes = SelectMultipleField('Ingredientes', choices=[("Jamon", "Jamon $10"), ("Piña", "Piña $10"), ("Champiñones", "Champiñones $10")],
                                                                widget=widgets.ListWidget(prefix_label=False),
                                                                option_widget=widgets.CheckboxInput())
    cantidad = IntegerField('Numero de pizzas', [
        validators.number_range(min=1, max=1000, message="Valor no valido")
    ])
    subTotal = IntegerField('SubTotal', [
        validators.number_range(min=1, max=1000, message="Valor no valido")
    ])
    nombre = StringField("Nombre",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")
    ])
    direccion = StringField("Direccion",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")
    ])
    tel = StringField("Telefono",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")
    ])
    fecha = DateField("Fecha",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")
    ])

class busqueda(Form):
    palabra = StringField("Ingresa el dia o mes",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")])
    fecha = DateField("Fecha",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")])
    filtro = RadioField('Filtro', choices=[("1", 'Dia'), ("2",'Mes')])