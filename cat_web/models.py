from itsdangerous import TimedJSONWebSignatureSerializer as seralizer
from cat_web import db,login_manager,app
from flask_login import UserMixin
from sqlalchemy import text

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    #__bind_key__ = 'anali'
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


#database dvdrenatal progresql
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
    nombre = db.Column(db.String(50),nullable=False)
    LastName = db.Column(db.String(50),nullable=False)
    Country   =db.Column(db.String(50),nullable=False)
    Email  =db.Column(db.String(50),nullable=False)
    def __init__(self, nombre, LastName, Country,Email):
        self.nombre = nombre
        self.LastName = LastName
        self.Country = Country
        self.Email = Email
    def __repr__(self):
        return '<ID_Cliente{}>'.format(self.ID_Cliente) 
# New Table from Database containe with database from diferent DatabaseManager
class ClientesA(db.Model):
    __bind_key__ = 'anali'
    ID_Cliente = db.Column(db.Integer,primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    Country   =db.Column(db.String(50))
    Email  =db.Column(db.String(50))
    def __init__(self, FirstName, LastName, Email, Country):
        self.Firstname = FirstName
        self.LastName = LastName
        self.Email = Email
        self.Country = Country
    def __repr__(self):
        return '<ID_Cliente{}>'.format(self.ID_Cliente) 

def usa_info():
    try:
        sql = text("SELECT [CustomerID],[Person].[Person].[FirstName],[Person].[Person].[LastName],Sales.SalesTerritory.Name,Person.[EmailAddress].EmailAddress FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].Person.Person  ON [AdventureWorks2017].[Sales].[Customer].PersonID = [AdventureWorks2017].Person.Person.BusinessEntityID INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID INNER JOIN [AdventureWorks2017].[Person].[EmailAddress] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[EmailAddress].BusinessEntityID where Sales.SalesTerritory.CountryRegionCode = 'US'; ")
        sql_m = text("SELECT [CustomerID],[Person].[Person].[FirstName],[Person].[Person].[LastName],Sales.SalesTerritory.Name,Person.[EmailAddress].EmailAddress FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].Person.Person  ON [AdventureWorks2017].[Sales].[Customer].PersonID = [AdventureWorks2017].Person.Person.BusinessEntityID INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID INNER JOIN [AdventureWorks2017].[Person].[EmailAddress] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[EmailAddress].BusinessEntityID where NOT Sales.SalesTerritory.CountryRegionCode = 'US'; ")
        data_USA = db.get_engine(bind='mssql').execute(sql)
        data_all = db.get_engine(bind='mssql').execute(sql_m)
        #datos_clienteM = ClienteM.query.filter_by(Country = 'United States').all()
        datos_clienteM = ClienteM.query.all()
        if datos_clienteM:
            return datos_clienteM
        else:
             for u in data_USA:
                    clientee = ClienteM(u[1],u[2],"United States",u[4])
                    db.session.add(clientee)
                    db.session.commit()
             for c in data_all:
                clin2 = ClienteM(c[1],c[2],c[3],c[4])
                db.session.add(clin2)
                db.session.commit()   
             db.session.close()
             return datos_clienteM   
    except IndentationError:
        db.session.rollback()
        return None
#Agreagr los datos en nueva tablas para anbas base de datos
def add_tablePos():
     try:
         slq_pos = text("SELECT customer_id, first_name, last_name, email,  public.country.country FROM public.customer INNER JOIN public.address ON public.customer.address_id = public.address.address_id INNER JOIN public.city on public.city.city_id =  public.address.city_id INNER JOIN public.country ON public.country.country_id = public.city.country_id;")
         #Database Posgresql
         datos_ClienteP = ClienteP.query.all()
         existe = hasattr(datos_ClienteP,"an_attribute")
         if datos_ClienteP:
                return datos_ClienteP
         else:
                pos_d = db.session.execute(slq_pos)
                for bd in pos_d:
                   todo_pos = ClienteP(bd[1],bd[2],bd[3],bd[4])
                   db.session.add(todo_pos)
                   db.session.commit()
                   db.session.close()
                
                return datos_ClienteP   
     except IndentationError:
        db.session.rollback()
        return None     

    