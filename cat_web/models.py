from itsdangerous import TimedJSONWebSignatureSerializer as seralizer
from cat_web import db,login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(20),unique=True,nullable=False)
    email= db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(150),nullable=False,default='https://res.cloudinary.com/pixies/image/upload/v1602729197/project/df_xbqa96.jpg')
    public_id = db.Column(db.String(120),default='project/df_xbqa96')
    password = db.Column(db.String(60),nullable=False)
    
    def get_reset_token(self,expires_sec=1800):
        s = seralizer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
        
    @staticmethod
    def verify_reset_token(token):
         s = seralizer(app.config['SECRET_KEY'])
         try:
             user_id = s.loads(token)['user_id']
         except:
            return None
         return User.query.get(user_id)   


    def __repr__(self):
        return f"User( '{self.username}','{self.email}','{self.image_file}')"


class ClienteP(db.Model):
    __tablename__ = 'Cliente'
    cliente_id =db.Column(db.Integer,primary_key=True)
    Firstname = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    Email  = db.Column(db.String(50))
    Country = db.Column(db.String(50))
    def __init__(self,FirstName,LastName,Email,Country):
        self.Firstname = FirstName
        self.LastName = LastName
        self.Email = Email
        self.Country = Country
    def __repr__(self):
        return '<cliente_id{}>'.format(self.cliente_id)

# Model from mssql database AdventureWorks2017 
class ClienteM(db.Model):
    __bind_key__ = 'mssql'
    __tablename__ = 'cliente'
    ID_Cliente = db.Column(db.Integer,primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    Country   =db.Column(db.String(50))
    Email  =db.Column(db.String(50))
    def __init__(cls, FirstName, LastName, Email, Country):
        self.Firstname = FirstName
        self.LastName = LastName
        self.Email = Email
        self.Country = Country
    def __repr__(self):
        return '<ID_Cliente{}>'.format(self.ID_Cliente)    