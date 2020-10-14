import os
import secrets
from flask import render_template, url_for,flash,redirect,request
from cat_web import app,db,bcrypt
from cat_web.forms import RegistrationForm,LoginForm,UpdateCuentaForm
from cat_web.models import User
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
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    
@app.route('/informacion_usuario',methods=['GET','POST'])
@login_required
def usuario():
    form= UpdateCuentaForm()
    if form.validate_on_submit():
        if form.foto.data:
            pass
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Tu cuenta fue actualizada exitosamente','success')
        redirect(url_for('usuario'))
    elif request.method == 'GET':
        form.username.data =  current_user.username
        form.email.data = current_user.email

    image_file = url_for('static',filename='profile_img/'+ current_user.image_file)
    return render_template('user_info.html',
                           image_file = image_file,form=form)

@app.route('/logout')
def salir_sesion():
    logout_user()
    return redirect(url_for('index'))

