from ast import dump
import os
import datetime
from os import kill
import secrets
import pandas as pd
from flask import render_template, url_for,flash,redirect,request,json,jsonify,make_response
from cat_web import app,db,bcrypt,cloud
from sqlalchemy import text
import cloudinary.uploader
from cat_web.forms import RegistrationForm,LoginForm,UpdateCuentaForm,RequestResetForm,ResetPasswordForm
from cat_web.models import User,ClienteM,ClienteP,ClientesA,todosDatos,groupByPais,dataforMap,dataMap,calcularThreeM,KlienteA,insert_Alld,firstTendatos,PDF,analizis,datos_agrupados_porPais
from flask_login import login_user,current_user,logout_user,login_required
import pdfkit



@app.route('/',methods=['GET','POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        usuarios = User.query.filter_by(email=form.email.data).first()
        if usuarios and bcrypt.check_password_hash(usuarios.password,form.password.data):
            login_user(usuarios,remember=form.remember.data)
            return redirect(url_for('home_page'))
        else:  
            flash('Esta meco mijo esa no es carnal!! checa',category='error')    
    return render_template('home.html',form=form)

@app.route('/Registarte',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        has_contrasena = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        usuario = User(username=form.username.data, email=form.email.data,password=has_contrasena)
        db.session.add(usuario)
        db.session.commit()
        flash('Tu cuenta fue creada exitosamente, ya es posible iniciar sesion', category='success')
        return redirect(url_for('index'))
    return render_template('registerF.html',form=form)

@app.route('/Iniciar_sesion')
@login_required
def home_page():
    usario = current_user.username
    foto = current_user.image_file
    return render_template('inicio.html',usario=usario,foto=foto)

def save_foto(form_picture):
    subir = cloud.uploader.upload(form_picture,folder='project/',use_filename = True)
    ubicacion = subir.get('secure_url')
    identicacion = (subir.get('public_id'))
    #form_picture.save(subir.get('secure_url'))
    #form_id.save(subir.get('public_id'))
    return ubicacion,identicacion


@app.route('/informacion_usuario',methods=['GET','POST'])
@login_required
def usuario():
    form= UpdateCuentaForm()
    form.public_id.data = current_user.public_id
    
    if form.validate_on_submit():
        if form.foto.data:
           
            ubicacion,identificacion = save_foto(form.foto.data)
            current_user.image_file = ubicacion
            current_user.public_id = identificacion
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Tu cuenta fue actualizada exitosamente','success')
        redirect(url_for('usuario'))
    elif request.method == 'GET':
        form.username.data =  current_user.username
        form.email.data = current_user.email

    #image_file = url_for('static',filename='profile_img/'+ current_user.image_file)
    image_file = current_user.image_file
    return render_template('user_info.html',
                           image_file = image_file,form=form)

@app.route('/logout')
def salir_sesion():
    logout_user()
    return redirect(url_for('index'))

def send_reset_email(usr):
    pass

@app.route('/reset_password',methods=['GET','POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An Email Has been sent with instructions to reset your password')
    return render_template('reset_request.html',form=form)

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('that is invalid or expired','warning')
        return redirect(url_for('reset_password'))
    form = ResetPasswordForm()
    return render_template('reset_token.html',form=form) 


@app.route('/analis_tablas_mssql_and_posgresql',methods=['GET','POST'])
@login_required   
def analisis():
    #roshi =  ClienteM.query.all()
    sql = text("SELECT * FROM [AdventureWorks2017].[dbo].[cliente]")
    roshi = db.get_engine(bind='mssql').execute(sql)
    #datos
    estadi =  calcularThreeM()
    mean = estadi[0]
    mediana = estadi[1]
    modas = estadi[2]
    return render_template("an_tables.html",roshi=roshi,mean=mean,mediana=mediana,modas=modas,
                                grupo_mayor =datos_agrupados_porPais(1),grupo_menor=datos_agrupados_porPais(2),
                                grupo_moda=datos_agrupados_porPais(3))

@app.route('/json/en_mi_casa')
def showdd():
    db = analizis.query.all()
    if db:
        datos = [{"ID":a.ID_Cliente,"firstName":a.name,"email":a.email,"address":a.address,"zip":a.zip,"phone":a.phone,"ciudad":a.ciudad,"country":a.pais} for a in db]
        return jsonify({"data":datos})
    else:
        no_data = [{"id":"NO HAY DATOS","Pais":"NO HAY DATOS","Numero":"NO HAY DATOS"}]
        return jsonify({"data":no_data})
    
#url con los datos a analizar

@app.route('/analis_tablas_mssql')
def dMsql():
    dotos =  ClienteM.query.all()
    #existe = hasattr(dotos,"an_attribute")
    if dotos:
        datos = [{"ID":a.ID_Cliente,"FirstName":a.nombre,"LastName":a.LastName,"Country":a.Country,"Email":a.Email} for a in dotos]
        return jsonify({"data":datos})
    else:
        no_data = [{"id":"NO HAY DATOS","Pais":"NO HAY DATOS","Numero":"NO HAY DATOS"}]
        return jsonify({"data":no_data})

    
@app.route('/analis_tablas_pos')
def dpos():
    dotos =  ClienteP.query.all()
    #existe = hasattr(dotos,"an_attribute")
    if dotos:
        datos = [{"ID":a.cliente_id,"FirstName":a.Firstname,"LastName":a.LastName,"Country":a.Country,"Email":a.Email} for a in dotos]
        return jsonify({"data":datos})
    else:
        no_data = [{"id":"NO HAY DATOS","Pais":"NO HAY DATOS","Numero":"NO HAY DATOS"}]
        return jsonify({"data":no_data})

#unir los daos base de datos en una
@app.route('/analisUnidos')
def dcorporado():
    todos_Datos =  ClientesA.query.all()
    if todos_Datos:
        datos = [{"ID":a.ID_Cliente,"firstName":a.firstname,"lastName":a.lastname,"country":a.country,"email":a.email,"phone":a.phone} for a in todos_Datos]
        return jsonify({"data":datos})
    else:
          d = todosDatos()
          datos = [{"ID":a.ID_Cliente,"firstName":a.firstname,";lastName":a.lastname,"country":a.country,"email":a.email,"phone":a.phone} for a in todos_Datos]
    return jsonify({"data":datos})


@app.route('/todos_capo')
def kombine():
    todo = KlienteA.query.all()
    if todo:
       datos = [{"ID":a.ID_Cliente,"firstName":a.nombre,"email":a.email,"address":a.address,"zip":a.zips,"phone":a.phone,"ciudad":a.ciudad,"country":a.country} for a in todo]
       return jsonify({"data":datos})
    else:
        insert_Alld()
        datos = [{"ID":a.ID_Cliente,"firstName":a.nombre,"email":a.email,"address":a.address,"zip":a.zips,"phone":a.phone,"ciudad":a.ciudad,"country":a.country} for a in todo]
        return jsonify({"data":datos})



#son los datos agrupaso en json
@app.route('/paisAgrupado')
def paisG():
    datito = groupByPais()
    return jsonify({"data":datito})

#son los datos sin nombre variable en json en forma [{}]
@app.route('/pasitas')
def pmapa():
    da =dataforMap()
    return jsonify(da) 

#son los datos con nombre variable en json en forma [{}]
@app.route('/pasitas/mapi')
def mapita():
    das =dataMap()
    return jsonify(das)

#son los datos todos los paises del munod en codigo EU como ejemplo
@app.route('/codex')
def codeguito():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT,'static/data','names.json')
    dato = json.load(open(json_url))
    return dato

@app.route('/ncodes')
def codegui():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT,'static/data','reeves.json')
    dato = json.load(open(json_url))
    return jsonify(dato)

@app.route('/continents')
def continentss():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT,'static/data','continent.json')
    dato = json.load(open(json_url))
    return jsonify(dato)
#33333333333333333333333333333333333333333333333333333333333333

@app.route('/casassss')
def report():
    fecha = datetime.datetime.now()
    fechita = str(fecha.day) + '/'+ fecha.strftime("%A")+'/'+str(fecha.year)
    #datos del usarios
    usernombre = current_user.username
    emailus = current_user.email
    #fotos de la nube
    logo = cloud.CloudinaryImage("https://res.cloudinary.com/pixies/image/upload/v1605124737/project/lgogo_mychqs.png")
    mapfoto = cloud.CloudinaryImage("https://res.cloudinary.com/pixies/image/upload/v1605129072/project/mapita_jcb0cp.jpg")
     #datos de los paises
    numClients =  firstTendatos()
     #datos
    estadi =  calcularThreeM()
    mean = estadi[0]
    mediana = estadi[1]
    modas = estadi[2]
    return render_template('pdf_template.html',mediana=mediana,modas=modas,mean=mean
                                    ,numClients=numClients,fechita=fechita,usernombre=usernombre,emailus=emailus,logo=logo,mapfoto=mapfoto)  

'''
@app.route('/downlods')
def pdfDownload():
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdf = pdfkit.from_url('http://127.0.0.1:5000/reports',False,configuration=config,css=css)
    pdf = pdfkit.from_url('http://127.0.0.1:5000/casassss',False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response

'''
@app.route('/downlods')
def pdfDownload():
    #Fechas
    fecha = datetime.datetime.now()
    fechita = str(fecha.day) + '/'+ fecha.strftime("%A")+'/'+str(fecha.year)
    #datos del usarios
    usernombre = current_user.username
    emailus = current_user.email
    #datos de los paises
    numClients =  firstTendatos()
     #datos
    estadi =  calcularThreeM()

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.print_chapter(estadi,fechita,usernombre,emailus,numClients)
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response


def Rendereds():
    """
    Datos necesarios para generar el Reporte
    """
      #DAtos NEcesarios para el reporte
    fecha = datetime.datetime.now()
    fechita = str(fecha.day) + '/'+ fecha.strftime("%A")+'/'+str(fecha.year)
    #datos del usarios
    usernombre = current_user.username
    emailus = current_user.email
    #fotos de la nube
    logo = cloud.CloudinaryImage("https://res.cloudinary.com/pixies/image/upload/v1605124737/project/lgogo_mychqs.png")
    mapfoto = cloud.CloudinaryImage("https://res.cloudinary.com/pixies/image/upload/v1605129072/project/mapita_jcb0cp.jpg")
     #datos de los paises
    numClients =  firstTendatos()
     #datos
    estadi =  calcularThreeM()
    mean = estadi[0]
    mediana = estadi[1]
    modas = estadi[2]
    rendered = render_template('pdf_template.html',mediana=mediana,modas=modas,mean=mean
                                    ,numClients=numClients,fechita=fechita,usernombre=usernombre,emailus=emailus,logo=logo,mapfoto=mapfoto)
    return rendered



                                       