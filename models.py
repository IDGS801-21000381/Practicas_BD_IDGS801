from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime
db=SQLAlchemy()

class Empleados(db.Model):
    __tablename__='empleados'
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    direcccion=db.Column(db.String(50))
    telefono=db.Column(db.String(10))
    email=db.Column(db.String(50))
    sueldo=db.Column(db.Float)
    """"
    Actividad de la pizza
    """
class Cliente(db.Model):
  __tablename__='cliente'
  id=db.Column(db.Integer,primary_key=True)
  nombre=db.Column(db.String(50))
  direcccion=db.Column(db.String(50))
  telefono=db.Column(db.String(10))
  #pizzas = relationship('Pizza', back_populates='Cliente')

# class Pizza(db.Model):
#   __tablename__='pizzas'
#   id=db.Column(db.Integer,primary_key=True)
#   tamanopizza=db.Column(db.String(50))
#   ingrediente=db.Column(db.String(70))
#   numpizza=db.Column(db.Integer)
#   fecha=db.Column(db.Date)
#   subtotal=db.Column(db.Float)
#   idcliente=db.Column(db.Integer,ForeignKey('cliente.id'))
#   #Cliente = relationship('Cliente', back_populates='Pizza') 

## si use
class Pizza(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    tamanio=db.Column(db.String(50))
    ingredientes=db.Column(db.String(50))
    cantidad=db.Column(db.Integer)
    subTotal=db.Column(db.String(50))
    nombre=db.Column(db.String(50))
    direccion=db.Column(db.String(50))
    tel=db.Column(db.String(50))
    fecha = db.Column(db.String(50))
    create_date=db.Column(db.DateTime, default=datetime.datetime.now)