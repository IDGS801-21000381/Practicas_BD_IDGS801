from flask import Flask,render_template,request
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from wtforms import validators
 
from models import db
from models import Empleados

app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()
 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
 
@app.before_request
def before_request():
    print("before 1")
   
@app.after_request
def after_request(response):
    print("after 3")
    return response
 
@app.route("/")
def calor():
        return render_template("index.html")


@app.route('/index',methods=['GET', 'POST'])
def index():
     create_form=forms.UserForm2(request.form)
     if request.method=='POST':
          emp=Empleados(nombre=create_form.nombre.data,
                       direcccion=create_form.direcccion.data,
                       telefono=create_form.telefono.data,
                       email=create_form.email.data,
                       sueldo=create_form.sueldo.data)
          db.session.add(emp)
          db.session.commit()
     return render_template('index.html', form=create_form)

@app.route("/ABC_Completo",methods=["GET","POST"])
def ABCompleto():
     emp_form=forms.UserForm2(request.form)
     empleado=Empleados.query.all()

     return render_template("ABC_Completo.html",empleado=empleado)

if __name__== "__main__":
    csrf.init_app(app)
    db.init_app(app)
    

    with app.app_context():
         db.create_all()
    app.run()