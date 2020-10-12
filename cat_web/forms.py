from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(min=2,max=25)],render_kw={"placeholder":"Usuername"})
    email = StringField('Email',validators=[DataRequired(),Email()],render_kw={"placeholder":"Correo"})
    password = PasswordField('Password',validators=[DataRequired()],render_kw={"placeholder":"Contrasena"})
    Confirm_password = PasswordField('Confirm Password',
                                        validators=[DataRequired(),EqualTo('password')],render_kw={"placeholder":"Re Ingrese la contrasena"})
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()],render_kw={"placeholder":"Correo"})
    password = PasswordField('Password',validators=[DataRequired()],render_kw={"placeholder":"Contrasena"})
    remember = BooleanField('Remember ME')
    submit = SubmitField('Login')