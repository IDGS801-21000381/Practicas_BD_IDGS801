from flask import Flask,render_template,request
from flask import flash, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
ordenes = []
from wtforms import validators
from flask import request
from models import db
from models import Empleados
from models import Cliente
from models import Pizza
from datetime import datetime
from sqlalchemy import func


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
     #return render_template("pizzas.html",empleado=empleado)
   
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

   #####
#   actividad de la pizza
   ####


###
@app.route('/pizzas', methods=['GET', 'POST'])
def pizza():
    create_form = forms.UserForm3(request.form)
    ingre = 0
    if request.method == 'POST':
        # Verificar si el cliente ya existe en la base de datos
        cliente_existente = Cliente.query.filter_by(nombre=create_form.nombre.data,
                                                    direcccion=create_form.direcccion.data,
                                                    telefono=create_form.telefono.data).first()
        if cliente_existente:
            # Si el cliente existe, usar el cliente existente para crear la pizza
            cli = cliente_existente
        else:
            # Si el cliente no existe, crear un nuevo cliente
            cli = Cliente(nombre=create_form.nombre.data,
                          direcccion=create_form.direcccion.data,
                          telefono=create_form.telefono.data)
            db.session.add(cli)
            db.session.commit()

        ingredientes = []
        if create_form.jamon.data:
            ingredientes.append('Jamon')
            ingre += 10
        if create_form.pina.data:
            ingredientes.append('Piña')
            ingre += 10
        if create_form.champinon.data:
            ingredientes.append('Champiñon')
            ingre += 10

        ingrediente_str = ','.join(ingredientes) if isinstance(ingredientes, list) else ''
        subt = ((ingre + int(create_form.tamanopizza.data)) * create_form.numpizza.data)

        piz = Pizza(tamanopizza=create_form.tamanopizza.data,
                    ingrediente=ingrediente_str,
                    numpizza=create_form.numpizza.data,
                    fecha=create_form.fecha.data,
                    subtotal=subt,
                    idcliente=cli.id)
        db.session.add(piz)
        db.session.commit()
    create_form = forms.UserForm3(request.form)

    
    cliente_existente_id = Cliente.query.filter_by(nombre=create_form.nombre.data,
                                               direcccion=create_form.direcccion.data,
                                               telefono=create_form.telefono.data)\
                                     .with_entities(Cliente.id)\
                                     .scalar()
    # print("###################################Datos########################################")
    # print(cliente_existente_id)
    pizzas_idcliente = Pizza.query.filter_by(idcliente=cliente_existente_id).all()
    # print("**************************************************")
    # print(pizzas_idcliente)

    #print("###################################Datos########################################")
    # for pizza in pizzas_idcliente:
    #   print(pizza.tamanopizza, pizza.ingrediente, pizza.numpizza, pizza.fecha, pizza.subtotal)  
    # pizzas_lunes = Pizza.query.filter(func.DATE_FORMAT(Pizza.fecha, "%W") == "Friday").all()

    # # Iterar sobre las pizzas y mostrar sus atributos
    # for pizza in pizzas_lunes:
    #   print(pizza.tamanopizza, pizza.ingrediente, pizza.numpizza, pizza.fecha, pizza.subtotal)
   
   
    return render_template("pizzas.html", form=create_form, pizzas_idcliente=pizzas_idcliente)

@app.route('/pizzasde',methods=['GET','POST'])
def eliminarpizza():
    create_form = forms.UserForm3(request.form)
    rec_id_clie=""
    if request.method=='GET':
        id=request.args.get('id')
        pi = db.session.query(Pizza).filter(Pizza.id==id).first()
        rec_id_clie=pi.idcliente
            
    request.method='POST'    
    print(rec_id_clie)
        
    if request.method=='POST':
        print("**************************************************")
        db.session.delete(pi)
        db.session.commit()
    #print("###################################Datos########################################")

    #print("###################################Datos########################################")
    # print(cliente_existente_id)
  
    pizzas_idcliente = Pizza.query.filter_by(idcliente=rec_id_clie).all()
    #print(pizzas_idcliente)
    
    return render_template("pizzas.html", form=create_form, pizzas_idcliente=pizzas_idcliente)

    # print("###################################Datos########################################")
    # print(cliente_existente_id)
    
@app.route('/pizzaup',methods=['GET','POST'])
def modificarpizza():
     create_form=forms.UserForm3(request.form)
     rec_id_clie=""
     if request.method=='GET':
        id=request.args.get('id')
        # select *from alumnos where id== id
        emp = db.session.query(Pizza).filter(Pizza.id==id).first()
        
        rec_id_clie=emp.idcliente
        
        id_clie=emp.idcliente
        client = db.session.query(Cliente).filter(Cliente.id==id_clie).first()
        create_form.nombre.data=client.nombre
        create_form.direcccion.data=client.direcccion
        create_form.telefono.data=client.telefono
        

        if emp.tamanopizza =="40":
          create_form.tamanopizza.data=40
        elif emp.tamanopizza =="80":
          create_form.tamanopizza.data=80
        elif emp.tamanopizza =="120":
          create_form.tamanopizza.data=120
       
        # print("###########################")
        ingredientes_separados = emp.ingrediente.split(',')
        for ingrediente in ingredientes_separados:
          if ingrediente=="Jamon":
            #print(ingrediente)
            create_form.jamon.data=ingrediente
          elif ingrediente=="Piña":
            #print(ingrediente)
            create_form.pina.data=ingrediente
          elif ingrediente=="Champiñon":
            #print(ingrediente)
            create_form.champinon.data=ingrediente     

        create_form.numpizza.data=emp.numpizza
        create_form.fecha.data=emp.fecha
        
        # print("###########################")
        pizzas_idcliente = Pizza.query.filter_by(idcliente=rec_id_clie).all()
        # print(pizzas_idcliente)
    
     return render_template("pizzas.html", form=create_form, pizzas_idcliente=pizzas_idcliente)
   
@app.route('/pizzaact',methods=['GET','POST'])
def actpizzas():
     create_form=forms.UserForm3(request.form)
     request.method='POST'
     if request.method=='POST':
        id=create_form.id.data
        emp = db.session.query(Pizza).filter(Pizza.id==id).first()  
        print("###########################")
        print(create_form.tamanopizza.data)
        print("###########################")
        emp.tamanopizza=create_form.tamanopizza.data
        
        ingredientes = []
        if create_form.jamon.data:
            ingredientes.append('Jamon')
            ingre += 10
        if create_form.pina.data:
            ingredientes.append('Piña')
            ingre += 10
        if create_form.champinon.data:
            ingredientes.append('Champiñon')
            ingre += 10

        ingrediente_str = ','.join(ingredientes) if isinstance(ingredientes, list) else ''
        subt = ((ingre + int(create_form.tamanopizza.data)) * create_form.numpizza.data)
        
        emp.ingrediente=ingrediente_str
        emp.numpizza=create_form.numpizza.data
        emp.fecha=create_form.fecha.data
        emp.subtotal=subt
        emp.idcliente=emp.idcliente
        print("###########################")
        print(
          emp.tamanopizza,
          emp.ingrediente,
          emp.numpizza,
          emp.fecha,
          emp.subtotal,
          emp.idcliente)
        print("###########################")
        #db.session.commit()
        return redirect(url_for('ABCompleto'))
     return render_template('pizzas.html',form=create_form) 
   
@app.route("/ABC", methods=["GET", "POST"])
def abc():
    abc_form = forms.busqueda(request.form)
    f = abc_form.palabra.data
    c = (abc_form.filtro.data)
    t = 0
    if c != None:
        t = int(c)
        
    nombres_de_dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    nombres_de_meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    piz = []
    if request.method == 'POST' or "GET":
        if t == 1:
            dia_semana = nombres_de_dias.index(f.lower())
            # Filtrar las fechas que coincidan con el día de la semana
            piz = [pizza for pizza in Pizza.query.all() if datetime.strptime(pizza.fecha, "%Y-%m-%d").weekday() == dia_semana]
        elif t == 2:
            mes = nombres_de_meses.index(f.lower()) + 1  # Sumamos 1 porque los meses en Python van de 1 a 12
            # Filtrar las fechas que coincidan con el mes
            piz = [pizza for pizza in Pizza.query.all() if datetime.strptime(pizza.fecha, "%Y-%m-%d").month == mes]
        elif t == 3:
            año = int(f)
            # Filtrar las fechas que coincidan con el año
            piz = [pizza for pizza in Pizza.query.all() if datetime.strptime(pizza.fecha, "%Y-%m-%d").year == año]
        elif t == 0:
            piz = Pizza.query.all()
    res= 0
    for a in piz:
        res+= int(a.subTotal)
    return render_template("ABCVentas.html",  bus=abc_form, Pizzas=piz, t = res)


@app.route("/pizza", methods=["GET", "POST"])
def pizza():
    nombreL = ""
    direccionL = ""
    telL = ""
    fechaL = ""

    totales_por_nombre = {}
    total = 0
    pizBD = Pizza.query.all()
    fecha_de_hoy = str(datetime.now().date())
    for pizza in pizBD:
        if pizza.fecha == fecha_de_hoy:
            nombre = pizza.nombre
            valor = int(pizza.subTotal)
            total += valor
            if nombre in totales_por_nombre:
                totales_por_nombre[nombre] += valor
            else:
                totales_por_nombre[nombre] = valor
    datos_objetos = [{'nombre': nombre, 'total': total} for nombre, total in totales_por_nombre.items()]
    pizza_form=forms.Pizza(request.form)
    np = {}
    if request.method=='POST':
        subtotal=0
        tamanio = pizza_form.tamanio.data
        nombreL = pizza_form.nombre.data
        direccionL = pizza_form.direccion.data
        telL = pizza_form.tel.data
        tamanio = pizza_form.tamanio.data
        fechaL = str(pizza_form.fecha.data)
        tamN = 0
        
        ingredientes = quit(str(pizza_form.ingredientes.data))
        cantidad = pizza_form.cantidad.data
        if tamanio == "Chica":
            tamN = 40
        elif tamanio == "Mediana":
            tamN = 80
        else:
            tamN = 120
        
        # subtotal = (tamN + int(ingredientes)) * int(cantidad)
        print(ingredientes.split(','))
        nt = ingredientes.split(',')
        if nt.__len__() == 1:
            n = 10
        elif nt.__len__() == 2:
            n = 20
        elif nt.__len__() == 3:
            n = 30
            
        subtotal = (tamN + n) * int(cantidad)
# Agrega más condici
        ordenes.append({'tamanio': tamanio, 'ingredientes': ingredientes, 'cantidad': cantidad, 'subtotal': subtotal,'nombre': nombreL, 'direccion': direccionL, 'tel': telL, 'fecha': fechaL})
        pizza_form.tamanio.data = None
        pizza_form.ingredientes.data = None
        pizza_form.cantidad.data = None
    return render_template("Pizzeria.html", Pizza = pizza_form, Ordenes = ordenes, NP = datos_objetos, Total = total, nombre = nombreL)

@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    posicion = int(request.args.get('id'))
    if request.method=='GET':
        ordenes.pop(posicion)
    return redirect("/pizza")

@app.route("/guardarP", methods=["GET", "POST"])
def guardarP():
    pizza_form = forms.Pizza(request.form)
    if request.method == 'POST' or "GET":
        print("De aqui")
        print(ordenes)
        for i in ordenes:
            pizza = Pizza(tamanio=i['tamanio'], ingredientes=i['ingredientes'], cantidad=i['cantidad'], subTotal=i['subtotal'], nombre=i["nombre"], direccion=i["direccion"], tel=i["tel"], fecha= i["fecha"])
            db.session.add(pizza)
            db.session.commit()
    ordenes.clear()
    return redirect("/pizza")

from datetime import datetime

@app.route("/ABC", methods=["GET", "POST"])
def abc():
    abc_form = forms.busqueda(request.form)
    f = abc_form.palabra.data
    c = (abc_form.filtro.data)
    t = 0
    if c != None:
        t = int(c)
        
    nombres_de_dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sábado', 'domingo']
    nombres_de_meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    piz = []
    if request.method == 'POST' or "GET":
        if t == 1:
            dia_semana = nombres_de_dias.index(f.lower())
            # Filtrar las fechas que coincidan con el día de la semana
            piz = [pizza for pizza in Pizza.query.all() if datetime.strptime(pizza.fecha, "%Y-%m-%d").weekday() == dia_semana]
        elif t == 2:
            mes = nombres_de_meses.index(f.lower()) + 1  # Sumamos 1 porque los meses en Python van de 1 a 12
            # Filtrar las fechas que coincidan con el mes
            piz = [pizza for pizza in Pizza.query.all() if datetime.strptime(pizza.fecha, "%Y-%m-%d").month == mes]
        # elif t == 3:
        #     año = int(f)
        #     # Filtrar las fechas que coincidan con el año
        #     piz = [pizza for pizza in Pizza.query.all() if datetime.strptime(pizza.fecha, "%Y-%m-%d").year == año]
        elif t == 0:
            piz = Pizza.query.all()
    res= 0
    for a in piz:
        res+= int(a.subTotal)
    return render_template("ABCVentas.html",  bus=abc_form, Pizzas=piz, t = res)



@app.route("/limp",  methods=("GET", "POST"))
def limp():
    pizza_form=forms.Pizza(request.form)
    pizza_form.tamanio.data = None
    pizza_form.ingredientes.data = None
    pizza_form.cantidad.data = None
    pizza_form.nombre.data = None
    pizza_form.direccion.data = None
    pizza_form.tel.data = None
    ordenes.clear()
    return redirect("/pizza")

def quit(cadena):
    cadena_sin_especiales = cadena.replace('[', '').replace(']', '').replace('"', '').replace("'", '')
    return cadena_sin_especiales




###
if __name__== "__main__":
    csrf.init_app(app)
    db.init_app(app)
    

    with app.app_context():
         db.create_all()
    app.run()