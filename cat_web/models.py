import os
import pycountry_convert as pc
from itsdangerous import TimedJSONWebSignatureSerializer as seralizer
from cat_web import db,login_manager,app
from flask_login import UserMixin
from sqlalchemy import text
import statistics

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
    __tablename__ = 'clientes'
    ID_Cliente = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    country   =db.Column(db.String(50))
    email  =db.Column(db.String(50))
    phone  =db.Column(db.String(50))
    def __init__(self, firstname, lastname, email, country,phone):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.country = country
        self.phone = phone
    def __repr__(self):
        return '<ID_Cliente{}>'.format(self.ID_Cliente) 

#modelos estranos alv 

#database dvdrenatal progresql la verdadera
class KlyentP(db.Model):
    __tablename__ = 'clyents'
    cliente_id =db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(50),nullable=False)
    email  = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(50),nullable=False)
    zips = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.String(50),nullable=False)
    ciudad =db.Column(db.String(50),nullable=False)
    Country   =db.Column(db.String(50),nullable=False)
    def __init__(self, nombre, email, address,zips,phone,ciudad,Country):
        self.nombre = nombre
        self.email = email
        self.address = address
        self.zips = zips
        self.phone = phone
        self.ciudad = ciudad
        self.Country = Country
    def __repr__(self):
        return '<cliente_id{}>'.format(self.cliente_id)        

# Model from mssql database AdventureWorks2017 
class KlyentM(db.Model):
    __bind_key__ = 'mssql'
    __tablename__ = 'clyent'
    ID_Cliente = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(50),nullable=False)
    email  = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(50),nullable=False)
    zips = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.String(50),nullable=False)
    ciudad =db.Column(db.String(50),nullable=False)
    Country   =db.Column(db.String(50),nullable=False)
    def __init__(self, nombre, email, address,zips,phone,ciudad,Country):
        self.nombre = nombre
        self.email = email
        self.address = address
        self.zips = zips
        self.phone = phone
        self.ciudad = ciudad
        self.Country = Country
        
    def __repr__(self):
        return '<ID_Cliente{}>'.format(self.ID_Cliente)

def usa_info():
    try:
        sql = text("SELECT [CustomerID],[Person].[Person].[FirstName],[Person].[Person].[LastName],Sales.SalesTerritory.Name,Person.[EmailAddress].EmailAddress FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].Person.Person  ON [AdventureWorks2017].[Sales].[Customer].PersonID = [AdventureWorks2017].Person.Person.BusinessEntityID INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID INNER JOIN [AdventureWorks2017].[Person].[EmailAddress] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[EmailAddress].BusinessEntityID where Sales.SalesTerritory.CountryRegionCode = 'US'; ")
        sql_m = text("SELECT [CustomerID],[Person].[Person].[FirstName],[Person].[Person].[LastName],Sales.SalesTerritory.Name,Person.[EmailAddress].EmailAddress FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].Person.Person  ON [AdventureWorks2017].[Sales].[Customer].PersonID = [AdventureWorks2017].Person.Person.BusinessEntityID INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID INNER JOIN [AdventureWorks2017].[Person].[EmailAddress] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[EmailAddress].BusinessEntityID where NOT Sales.SalesTerritory.CountryRegionCode = 'US'; ")
        sql_all = text("SELECT [CustomerID],[Person].[Person].[FirstName],[Person].[Person].[LastName],Sales.SalesTerritory.Name,Person.[EmailAddress].EmailAddress,[Person].[PersonPhone].[PhoneNumber] FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].Person.Person  ON [AdventureWorks2017].[Sales].[Customer].PersonID = [AdventureWorks2017].Person.Person.BusinessEntityID INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID INNER JOIN [AdventureWorks2017].[Person].[EmailAddress] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[EmailAddress].BusinessEntityID INNER JOIN [AdventureWorks2017].[Person].[PersonPhone] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[PersonPhone].BusinessEntityID where NOT Sales.SalesTerritory.CountryRegionCode = 'US';")
        sql_us = text("SELECT [CustomerID],[Person].[Person].[FirstName],[Person].[Person].[LastName],Sales.SalesTerritory.Name,Person.[EmailAddress].EmailAddress,[Person].[PersonPhone].[PhoneNumber] FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].Person.Person  ON [AdventureWorks2017].[Sales].[Customer].PersonID = [AdventureWorks2017].Person.Person.BusinessEntityID INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID INNER JOIN [AdventureWorks2017].[Person].[EmailAddress] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[EmailAddress].BusinessEntityID INNER JOIN [AdventureWorks2017].[Person].[PersonPhone] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[PersonPhone].BusinessEntityID where  Sales.SalesTerritory.CountryRegionCode = 'US';")
        sql_null1 = text("SELECT [CustomerID] ,Sales.SalesTerritory.Name FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID where [PersonID]  is NULL AND Sales.SalesTerritory.CountryRegionCode = 'US'")
        sql_null2 = text("SELECT [CustomerID] ,Sales.SalesTerritory.Name FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID where [PersonID]  is NULL AND NOT Sales.SalesTerritory.CountryRegionCode = 'US'")
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

#modelo que si vamos usar jaja
class KlienteA(db.Model):
    __bind_key__ = 'anali'
    __tablename__ = 'klyients'
    ID_Cliente = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(50),nullable=False)
    email  = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(50),nullable=False)
    zips = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.String(50),nullable=False)
    ciudad =db.Column(db.String(50),nullable=False)
    country   =db.Column(db.String(50),nullable=False)
    def __init__(self, nombre, email, address,zips,phone,ciudad,country):
        self.nombre = nombre
        self.email = email
        self.address = address
        self.zips = zips
        self.phone = phone
        self.ciudad = ciudad
        self.country = country
    def __repr__(self):
        return '<ID_Cliente{}>'.format(self.ID_Cliente)


class Continek(db.Model):
    __bind_key__ = 'anali'
    __tablename__ = 'coninek'
    ID_continent = db.Column(db.Integer,primary_key=True)
    country   =db.Column(db.String(50),nullable=False)
    code = db.Column(db.String(50),nullable=False)
    numclients = db.Column(db.Integer)
    def __init__(self,country,code,numclients):
        self.country = country
        self.code = code
        self.numclients = numclients
    def __repr__(self):
       return '<ID_continent{}>'.format(self.ID_continent)

#metodo para insertar datos
def todosDatos():
        sql_all = text("SELECT [CustomerID],[Person].[Person].[FirstName],[Person].[Person].[LastName],Sales.SalesTerritory.Name,Person.[EmailAddress].EmailAddress,[Person].[PersonPhone].[PhoneNumber] FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].Person.Person  ON [AdventureWorks2017].[Sales].[Customer].PersonID = [AdventureWorks2017].Person.Person.BusinessEntityID INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID INNER JOIN [AdventureWorks2017].[Person].[EmailAddress] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[EmailAddress].BusinessEntityID INNER JOIN [AdventureWorks2017].[Person].[PersonPhone] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[PersonPhone].BusinessEntityID where NOT Sales.SalesTerritory.CountryRegionCode = 'US';")
        sql_us = text("SELECT [CustomerID],[Person].[Person].[FirstName],[Person].[Person].[LastName],Sales.SalesTerritory.Name,Person.[EmailAddress].EmailAddress,[Person].[PersonPhone].[PhoneNumber] FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].Person.Person  ON [AdventureWorks2017].[Sales].[Customer].PersonID = [AdventureWorks2017].Person.Person.BusinessEntityID INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID INNER JOIN [AdventureWorks2017].[Person].[EmailAddress] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[EmailAddress].BusinessEntityID INNER JOIN [AdventureWorks2017].[Person].[PersonPhone] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[PersonPhone].BusinessEntityID where  Sales.SalesTerritory.CountryRegionCode = 'US';")
        sql_null1 = text("SELECT [CustomerID] ,Sales.SalesTerritory.Name FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID where [PersonID]  is NULL AND Sales.SalesTerritory.CountryRegionCode = 'US'")
        sql_null2 = text("SELECT [CustomerID] ,Sales.SalesTerritory.Name FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID where [PersonID]  is NULL AND NOT Sales.SalesTerritory.CountryRegionCode = 'US'")
        slq_pos = text("SELECT customer_id, first_name, last_name, public.country.country,email,phone   FROM public.customer INNER JOIN public.address ON public.customer.address_id = public.address.address_id INNER JOIN public.city on public.city.city_id =  public.address.city_id INNER JOIN public.country ON public.country.country_id = public.city.country_id;")
        data_USA = db.get_engine(bind='mssql').execute(sql_us)
        data_all = db.get_engine(bind='mssql').execute(sql_all)
        data_all2 = db.get_engine(bind='mssql').execute(sql_null2)
        data_USA2 = db.get_engine(bind='mssql').execute(sql_null1)
        pos = db.engine.execute(slq_pos)
        #Database Posgresql

        f = open('sol.txt','w')

        for u in data_USA:
            f.write(str(u[1]) + ','+str(u[2])+ ','+'United States'+ ','+str(u[4])+ ','+str(u[5]) + '\n')
        f.close()
        
        f2 = open('sol.txt','a')
        for a in data_all:
            f2.write(str(a[1]) + ','+str(a[2])+ ','+str(a[3])+ ','+str(a[4])+ ','+str(a[5]) + '\n')
        f2.close()
        
        f3 = open('sol.txt','a')
        for x in data_USA2:
            f3.write('' + ','+''+ ','+'United States'+ ','+''+ ','+''+ '\n')
        f3.close()
        
        f4 = open('sol.txt','a')
        for r in data_all2:
            f4.write('' + ','+''+ ','+str(r[1])+ ','+''+ ','+''+ '\n')
        f4.close()

        f5 = open('sol.txt','a')
        if pos:
            print("si hay we ")
        else:
            print("No hay")    
        for g in pos:
            f5.write(str(g[1]) + ','+str(g[2])+ ','+str(g[3])+ ','+str(g[4])+ ','+str(g[5]) + '\n')
        f5.close()
        #convertir el archivo texto a utf8
        os.system('powershell.exe Get-Content sol2.txt -Encoding Oem ^| Out-File lgs.txt -Encoding utf8')
        #insertar todos los datos a la nueva base de datos
        nsql = text("copy public.clientes (firstName, lastName, country, email, phone) from 'D:\Development\Python\Catweb\yaw_data.txt'  DELIMITER ',';commit;")
        doll = db.get_engine(bind='anali').execute(nsql)
      

#se aagrupan los datos por pais
def groupByPais():
    querie = text("SELECT country, COUNT('ID_Cliente') as cliente FROM public.klyients GROUP BY country ORDER BY cliente DESC;")
    
    data_USA2 = db.get_engine(bind='anali').execute(querie)
    #anali
    if data_USA2:
        datos = [{"Pais":a[0],"NumeroClientes":a[1]} for a in data_USA2]
        return datos
    else:
        no_data = [{"Pais":"NO HAY DATOS","NumeroClientes":"NO HAY DATOS"}]
        return no_data

#get data by conutry
def  continent():
    querie = text("SELECT country, COUNT('ID_Cliente') as cliente FROM public.klyients GROUP BY country ORDER BY cliente DESC;")
    data_USA2 = db.get_engine(bind='anali').execute(querie)
    caontien ={}

    for a in data_USA2:
        rufles = get_continent(a[0])
        roco = Continek(a[0],rufles,a[1])
        db.session.add(roco)
        db.session.commit()
    db.session.close()
def get_continent(col):
    try:
        cn_a2_code =  pc.country_name_to_country_alpha2(col)
    except:
        cn_a2_code = 'Unknown' 
    try:
        cn_continent = pc.country_alpha2_to_continent_code(cn_a2_code)
    except:
        cn_continent = 'Unknown'
    return  cn_continent 

#se calcula estadistica de media,moda y mediana
def calcularThreeM():
    querie = text("SELECT country, COUNT('ID_Cliente') as cliente FROM public.klyients GROUP BY country ORDER BY cliente DESC;")
    data = db.get_engine(bind='anali').execute(querie)
    sumita =0
    sumisa = []
    for t in data:
        sumisa.append(t[1])
    sd = statistics.mean(sumisa)
    mean = round(sd,2)
    print("Media del: " , mean)
    mediana = statistics.median(sumisa)
    print("Mediana: ",mediana)
    modas = statistics.mode(sumisa)
    print("Moda",modas)
    estadistica = [mean,mediana,modas]
    return estadistica

#datos para el maapa
def dataforMap():
    querie = text("SELECT country, COUNT('ID_Cliente') as cliente FROM public.klyients GROUP BY country ORDER BY cliente DESC;")
    data = db.get_engine(bind='anali').execute(querie)
    resultado = [{sa[0]:sa[1]} for sa in data]
    return resultado

#datos del mapa
def dataMap():
    querie = text("SELECT country, COUNT('ID_Cliente') as cliente FROM public.klyients GROUP BY country ORDER BY cliente DESC;")
    data = db.get_engine(bind='anali').execute(querie)
    resultado = [{"Pais":sa[0],"NumeroClientes":sa[1]} for sa in data]
    return resultado

#Vamos a crear Datos mamalones
def insert_Alld():
    q = text("COPY public.klyients( nombre, email, address, zips, phone, ciudad, country) FROM 'D:\Development\Python\Catweb\msnas.csv' DELIMITER ',' CSV HEADER;commit;")
    doll = db.get_engine(bind='anali').execute(q)


def firstTendatos():
    query = text("SELECT country, COUNT('ID_Cliente') as cliente FROM public.klyients GROUP BY country ORDER BY cliente DESC FETCH FIRST 10 ROWS ONLY;")
    paisbyCl = db.get_engine(bind='anali').execute(query)
    return paisbyCl
