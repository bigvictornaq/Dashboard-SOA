from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from cat_web.models import User

class RegistrationForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(min=2,max=25)],render_kw={"placeholder":"Usuername"})
    email = StringField('Email',validators=[DataRequired(),Email()],render_kw={"placeholder":"Correo"})
    password = PasswordField('Password',validators=[DataRequired()],render_kw={"placeholder":"Contrasena"})
    Confirm_password = PasswordField('Confirm Password',
                                        validators=[DataRequired(),EqualTo('password')],render_kw={"placeholder":"Re Ingrese la contrasena"})
    submit = SubmitField('Sign up')

    def validate_username(self,username):
        uuario = User.query.filter_by(username=username.data).first()
        if uuario:
            raise ValidationError('That usario ya existe por favor agregue al decente')
    def validate_email(self,email):
        uuario = User.query.filter_by(email=email.data).first()
        if uuario:
            raise ValidationError('That Correo ya existe por favor agregue al decente')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()],render_kw={"placeholder":"Correo"})
    password = PasswordField('Password',validators=[DataRequired()],render_kw={"placeholder":"Contrasena"})
    remember = BooleanField('Remember ME')
    submit = SubmitField('Login')