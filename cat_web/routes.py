from flask import render_template, url_for,flash,redirect
from cat_web import app
from cat_web.forms import RegistrationForm,LoginForm
from cat_web.models import User



@app.route('/',methods=['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'coco@pixies.com' and form.password.data == '123':
            flash("A perro sabes la tecnica",category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Esta meco mijo esa no es carnal!! checa',category='error')    
    return render_template('home.html',form=form)

@app.route('/Registarte',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Cuenta fue creada para {form.username.data}!', category='success')
        return redirect(url_for('index'))
    return render_template('registerF.html',form=form)

@app.route('/Iniciar_sesion')
def home_page():
    return "Eres el mejor perro"

    return"hola ese"