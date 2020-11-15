import os
import pycountry_convert as pc
import pandas as pd
from fpdf import FPDF
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

#Creacion del template PDF
class PDF(FPDF):
    #Encabezado del pdf
    def header(self):
        # Logo
        self.image('cat_web\static\profile_img\lgogo.png', 165, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 25)
        # Se mueve a la derecha
        self.cell(80)
        # Titulo
        self.cell(30, 49, 'Reporte de Analisis de datos', 0, 0, 'C')
        # Line break
        self.ln(20)

    def chapter_body(self,estadistica,date,user,email,num_clients):
        self.ln(10)
        # Times 12
        self.set_font('Times', '', 12)
        self.cell(0,8,"Nombre del Proyecto: Generacion de PDF template con informacion con base de datos",1,1)
        self.set_font('Times', '', 12)
        self.cell(0,8,"Nombre de Reporte: ",1,1)
        self.set_font('Times', '', 12)
        self.cell(150,-8,f"Fecha: {date}",0,0,"R")
        self.ln(2)
        self.set_font('Times', '', 12)
        self.cell(0,8,f"{user}",0,0)
        # Linea horizontal
        self.line(10,68,200,68)
        
        self.ln(8)
        self.set_font('Times', 'I', 12)
        self.cell(0,8,"Nombre Usario quien realizo la consulta",0,0)
        self.ln(10)
        self.set_font('Times', '', 12)
        self.cell(0,8,f"{email}",0,0)
        # Linea horizontal
        self.line(10,85,200,85)
        self.ln(8)
        self.set_font('Times', 'I', 12)
        self.cell(0,8,"Correo Electronico del Usario ",0,0)
        self.ln(8)
        self.set_font('Times','B',14)
        self.cell(78,50,"Proposito De la Investigacion datos",1,2)
        self.set_xy(88,92)
        self.set_font('Times', '', 12)
        texto = '''
 Nosotros previamente seleccionamos las tablas de cliente
 de ambas bases datos, con el objetivo buscar una
 estrategia para las diferentes áreas,en donde no tenga un
 gran impacto,por ejemplo,como los países con menos
 clientes de 20 o menos. Además de buscar un patrón en
 esos países no compiten con los países con mayores
 clientes. Dar unasoluciónpara fortalecer las áreas con
 menores clientes.
        '''
        self.multi_cell(112,5,texto,1,2,"L")
        self.ln()
        self.set_font('Times','B',14)
        self.cell(0,8,"Fase 2 Preprocesamiento",0,0)
        self.ln()
        self.set_font('Times','',12) 
        self.cell(0,8,"Conceptos",0,0)
        self.ln(-1)
        text2 = '''
Para poder comenzar a trabajar en la segunda fase se investigó sobre la media, mediana y moda, las cuales son la herramientanecesaria para poder observar que parte es en la que más me conviene trabajar
        '''
        self.set_font('Times','',12) 
        self.multi_cell(0,5,text2,0,0)
        self.ln()
        self.set_font('Times','',12)
        self.cell(0,8,f"Mediana: {estadistica[1]}",0,0)
        self.ln()
        self.set_font('Times','',12)
        self.cell(0,8,f"Media: {estadistica[0]}",0,0)
        self.ln()
        self.set_font('Times','',12)
        self.cell(0,8,f"Moda: {estadistica[2]}",0,0)
        self.ln(17)
        self.set_font('Times','B',14)
        self.cell(0,8,"Conslucion",0,0)
        self.ln(5)
        #tratar de hacer una tabla
        self.set_font('Times','',12)
        th = self.font_size
        num=0
        for row in num_clients:
            num = num + 8
            self.set_xy(120,170 + num)
            for dats in row:              
                self.cell(40,8,str(dats),1)
            self.ln()    
        #alternative
        self.ln(-5)    
                
    
    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    def print_chapter(self,estadistica,date,user,email,num_clients):
        self.add_page()
        self.chapter_body(estadistica,date,user,email,num_clients)    

#modelo que si vamos usar jaja
class analizis(db.Model):
    __bind_key__ = 'anali'
    __tablename__ = 'analisis'
    ID_Cliente = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email  = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(50),nullable=False)
    zip = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.String(50),nullable=False)
    ciudad =db.Column(db.String(50),nullable=False)
    pais   =db.Column(db.String(50),nullable=False)
    def __init__(self, name, email, address,zip,phone,ciudad,pais):
        self.name = name
        self.email = email
        self.address = address
        self.zips = zip
        self.phone = phone
        self.ciudad = ciudad
        self.pais = pais
    def __repr__(self):
        return '<ID_Cliente{}>'.format(self.ID_Cliente)

#Uso de dataframes con pandas
# con los dataframes se agrena en la nueva base de datos
# 
def create_dataframe_sql():
            #base de datos adventuresworks2017
            engine_pos = db.get_engine()
            enginen = db.get_engine(bind='anali')
            engine_ms = db.get_engine(bind='mssql')
            sql_query = pd.read_sql_query(
                '''with t1 as (Select *, p.FirstName+' '+p.LastName AS full_name from [AdventureWorks2017].Person.Person p)
                SELECT 
	            full_name as name,
	            em.EmailAddress as email,
	            addr.AddressLine1 as address,
		        addr.PostalCode as zip,
                pho.PhoneNumber as phone,
	            addr.City as ciudad,
	            cr.Name as pais	  
                FROM
                t1
	            INNER JOIN [AdventureWorks2017].Sales.Customer cu
                ON cu.PersonID = t1.BusinessEntityID
                INNER JOIN Person.EmailAddress em
                ON em.BusinessEntityID = t1.BusinessEntityID 
		        inner join Person.BusinessEntity bus
		        on bus.BusinessEntityID = t1.BusinessEntityID
                inner join Person.PersonPhone pho
                on pho.BusinessEntityID = t1.BusinessEntityID
                INNER join Person.BusinessEntityAddress bea
                on bea.BusinessEntityID = t1.BusinessEntityID
                INNER join Person.Address addr
                on bea.AddressID = addr.AddressID 
                INNER join sales.SalesTerritory st 
                on st.TerritoryID = cu.TerritoryID 
                INNER join Person.CountryRegion cr
		        on cr.CountryRegionCode	= st.CountryRegionCode ''',con=engine_ms)
                #base de datos dvdrental
            sql_q = pd.read_sql_query(
                '''with t1 as (Select *, first_name || ' ' || last_name AS full_name from customer)  
                select full_name as Name, email as Email, address as Address,postal_code as zip, phone as Phone, city as Ciudad, country as Pais
                from t1 
                Join address  using (address_id)    join city   using (city_id) join country using (country_id) 
                join payment 
                using(customer_id) 
                group by 1,2,3,4,5,6,7''',con=engine_pos)
                #insertar datos a la nueva base datos llamado analisis 
            sql_query.to_sql("analisis",con=enginen,if_exists="append",index=False)
            sql_q.to_sql("analisis",con=enginen,if_exists="append",index=False)

def ms_to_dataframe():
         engine_ms = db.get_engine(bind='mssql')
         sql_query = pd.read_sql_query(
                '''with t1 as (Select *, p.FirstName+' '+p.LastName AS full_name from [AdventureWorks2017].Person.Person p)
                SELECT 
	            full_name as name,
	            em.EmailAddress as email,
	            addr.AddressLine1 as address,
		        addr.PostalCode as zip,
                pho.PhoneNumber as phone,
	            addr.City as ciudad,
	            cr.Name as pais	  
                FROM
                t1
	            INNER JOIN [AdventureWorks2017].Sales.Customer cu
                ON cu.PersonID = t1.BusinessEntityID
                INNER JOIN Person.EmailAddress em
                ON em.BusinessEntityID = t1.BusinessEntityID 
		        inner join Person.BusinessEntity bus
		        on bus.BusinessEntityID = t1.BusinessEntityID
                inner join Person.PersonPhone pho
                on pho.BusinessEntityID = t1.BusinessEntityID
                INNER join Person.BusinessEntityAddress bea
                on bea.BusinessEntityID = t1.BusinessEntityID
                INNER join Person.Address addr
                on bea.AddressID = addr.AddressID 
                INNER join sales.SalesTerritory st 
                on st.TerritoryID = cu.TerritoryID 
                INNER join Person.CountryRegion cr
		        on cr.CountryRegionCode	= st.CountryRegionCode ''',con=engine_ms)
         return sql_query       


def pos_to_dataframe():
        engine_pos = db.get_engine()
        sql_querys = pd.read_sql_query(
            '''with t1 as (Select *, first_name || ' ' || last_name AS full_name from customer)  
            select full_name as Name, email as Email, address as Address,postal_code as zip, phone as Phone, city as Ciudad, country as Pais
            from t1 
            Join address  using (address_id)    join city   using (city_id) join country using (country_id) 
            join payment 
            using(customer_id) 
            group by 1,2,3,4,5,6,7''',con=engine_pos)
        return sql_querys


def insert():
    q = text("COPY public.analisis( name, email, address, zip, phone, ciudad, pais) FROM 'D:\Development\Python\Catweb\posgresal.csv' DELIMITER ',' CSV HEADER;commit;")
    doll = db.get_engine(bind='anali').execute(q)

def intete():
    q = text("COPY public.analisis( name, email, address, zip, phone, ciudad, pais) FROM 'D:\Development\Python\Catweb\msss.csv' DELIMITER ',' CSV HEADER;commit;")
    doll = db.get_engine(bind='anali').execute(q)


def create_dataframe_an():
    engine_an = db.get_engine(bind='anali')
    datafm = pd.read_sql_table('analisis',con=engine_an)
    return datafm

#Agregan los datos a la base de datos
def definitive_master():
     engine_ms = db.get_engine(bind='mssql')
     sql_query = pd.read_sql_query(
                '''with t1 as (Select *, p.FirstName+' '+p.LastName AS full_name from [AdventureWorks2017].Person.Person p)
                SELECT 
	            full_name as name,
	            em.EmailAddress as email,
	            addr.AddressLine1 as address,
		        addr.PostalCode as zip,
                pho.PhoneNumber as phone,
	            addr.City as ciudad,
	            cr.Name as pais	  
                FROM
                t1
	            INNER JOIN [AdventureWorks2017].Sales.Customer cu
                ON cu.PersonID = t1.BusinessEntityID
                INNER JOIN Person.EmailAddress em
                ON em.BusinessEntityID = t1.BusinessEntityID 
		        inner join Person.BusinessEntity bus
		        on bus.BusinessEntityID = t1.BusinessEntityID
                inner join Person.PersonPhone pho
                on pho.BusinessEntityID = t1.BusinessEntityID
                INNER join Person.BusinessEntityAddress bea
                on bea.BusinessEntityID = t1.BusinessEntityID
                INNER join Person.Address addr
                on bea.AddressID = addr.AddressID 
                INNER join sales.SalesTerritory st 
                on st.TerritoryID = cu.TerritoryID 
                INNER join Person.CountryRegion cr
		        on cr.CountryRegionCode	= st.CountryRegionCode ''',con=engine_ms)
     engine_pos = db.get_engine()
     sql_querys = pd.read_sql_query(
            '''with t1 as (Select *, first_name || ' ' || last_name AS full_name from customer)  
            select full_name as Name, email as Email, address as Address,postal_code as zip, phone as Phone, city as Ciudad, country as Pais
            from t1 
            Join address  using (address_id)    join city   using (city_id) join country using (country_id) 
            join payment 
            using(customer_id) 
            group by 1,2,3,4,5,6,7''',con=engine_pos)
     #create csv for load new database
    #se borra los archivos
     if os.path.isfile('D:\Development\Python\Catweb\msss.csv'):
         os.remove('D:\Development\Python\Catweb\msss.csv')
     if os.path.isfile('D:\Development\Python\Catweb\pss.csv'):
         os.remove('D:\Development\Python\Catweb\pss.csv')

     #se genera csv
     sql_query.to_csv('D:\Development\Python\Catweb\msss.csv',index=False)
     sql_querys.to_csv('D:\Development\Python\Catweb\pss.csv',index=False)

     #se agregan los datos a la nueva base de datos
     ms_data = text("COPY public.analisis( name, email, address, zip, phone, ciudad, pais) FROM 'D:\Development\Python\Catweb\msss.csv' DELIMITER ',' CSV HEADER;commit;")
     exc = db.get_engine(bind='anali').execute(ms_data)
     ps_data = text("COPY public.analisis( name, email, address, zip, phone, ciudad, pais) FROM 'D:\Development\Python\Catweb\pss.csv' DELIMITER ',' CSV HEADER;commit;")
     exc2 = db.get_engine(bind='anali').execute(ps_data)