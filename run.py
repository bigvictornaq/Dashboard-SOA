from flask import Flask,render_template, url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8d723bc78222badb938f27312dde8956'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ifxvfpua:4552V0r2IkVujztnh3F5puUE79kTmuQM@lallah.db.elephantsql.com:5432/ifxvfpua"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(20),unique=True,nullable=False)
    email= db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    
    def __repr__(self):
        return f"User( '{self.username}','{self.email}','{self.image_file}')"





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

if __name__ == '__main__':
    app.run(debug=True)
