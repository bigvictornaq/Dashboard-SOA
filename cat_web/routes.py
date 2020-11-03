import os
import secrets
from flask import render_template, url_for,flash,redirect,request,json,jsonify
from cat_web import app,db,bcrypt,cloud
from sqlalchemy import text
import cloudinary.uploader
from cat_web.forms import RegistrationForm,LoginForm,UpdateCuentaForm,RequestResetForm,ResetPasswordForm
from cat_web.models import User,ClienteM,ClienteP,ClientesA,todosDatos,groupByPais,dataforMap,dataMap
from flask_login import login_user,current_user,logout_user,login_required



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
    return render_template('inicio.html')

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
    return render_template("an_tables.html",roshi=roshi)


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




@app.route('/paisAgrupado')
def paisG():
    datito = groupByPais()
    return jsonify({"data":datito})


@app.route('/pasitas')
def pmapa():
    da =dataforMap()
    return jsonify(da) 


@app.route('/pasitas/mapi')
def mapita():
    das =dataMap()
    return jsonify(das)        