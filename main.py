from flask import Flask,render_template,request
from flask import flash, redirect, url_for
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
   
@app.route('/eliminar',methods=['GET','POST'])
def eliminar():
     create_form=forms.UserForm2(request.form)
     if request.method=='GET':
        id=request.args.get('id')
        # select *from alumnos where id== id
        emp = db.session.query(Empleados).filter(Empleados.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=emp.nombre
        create_form.direcccion.data=emp.direcccion
        create_form.telefono.data=emp.telefono
        create_form.email.data=emp.email
        create_form.sueldo.data=emp.sueldo

     if request.method=='POST':
        id=create_form.id.data
        emp= Empleados.query.get(id) 
        #delete from alumnos where id=id
        db.session.delete(emp)
        db.session.commit()
        return redirect(url_for('ABCompleto'))
     return render_template('eliminar.html',form=create_form)   

@app.route('/modificar',methods=['GET','POST'])
def modificar():
     create_form=forms.UserForm2(request.form)
     if request.method=='GET':
        id=request.args.get('id')
        # select *from alumnos where id== id
        emp = db.session.query(Empleados).filter(Empleados.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=emp.nombre
        create_form.direcccion.data=emp.direcccion
        create_form.telefono.data=emp.telefono
        create_form.email.data=emp.email
        create_form.sueldo.data=emp.sueldo

     if request.method=='POST':
        id=create_form.id.data
        emp = db.session.query(Empleados).filter(Empleados.id==id).first()   
        emp.nombre=create_form.nombre.data
        emp.direcccion=create_form.direcccion.data
        emp.telefono=create_form.telefono.data
        emp.email=create_form.email.data
        emp.sueldo=create_form.sueldo.data
        db.session.add(emp)
        db.session.commit()
        return redirect(url_for('ABCompleto'))
     return render_template('modificar.html',form=create_form) 

   

if __name__== "__main__":
    csrf.init_app(app)
    db.init_app(app)
    

    with app.app_context():
         db.create_all()
    app.run()