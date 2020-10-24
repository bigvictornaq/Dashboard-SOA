from cat_web import db
from sqlalchemy import text


sql_all = text("SELECT [CustomerID],[Person].[Person].[FirstName],[Person].[Person].[LastName],Sales.SalesTerritory.Name,Person.[EmailAddress].EmailAddress,[Person].[PersonPhone].[PhoneNumber] FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].Person.Person  ON [AdventureWorks2017].[Sales].[Customer].PersonID = [AdventureWorks2017].Person.Person.BusinessEntityID INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID INNER JOIN [AdventureWorks2017].[Person].[EmailAddress] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[EmailAddress].BusinessEntityID INNER JOIN [AdventureWorks2017].[Person].[PersonPhone] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[PersonPhone].BusinessEntityID where NOT Sales.SalesTerritory.CountryRegionCode = 'US';")
sql_us = text("SELECT [CustomerID],[Person].[Person].[FirstName],[Person].[Person].[LastName],Sales.SalesTerritory.Name,Person.[EmailAddress].EmailAddress,[Person].[PersonPhone].[PhoneNumber] FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].Person.Person  ON [AdventureWorks2017].[Sales].[Customer].PersonID = [AdventureWorks2017].Person.Person.BusinessEntityID INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID INNER JOIN [AdventureWorks2017].[Person].[EmailAddress] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[EmailAddress].BusinessEntityID INNER JOIN [AdventureWorks2017].[Person].[PersonPhone] ON [AdventureWorks2017].Person.Person.BusinessEntityID =[AdventureWorks2017].[Person].[PersonPhone].BusinessEntityID where  Sales.SalesTerritory.CountryRegionCode = 'US';")
sql_null1 = text("SELECT [CustomerID] ,Sales.SalesTerritory.Name FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID where [PersonID]  is NULL AND Sales.SalesTerritory.CountryRegionCode = 'US'")
sql_null2 = text("SELECT [CustomerID] ,Sales.SalesTerritory.Name FROM [AdventureWorks2017].[Sales].[Customer] INNER JOIN [AdventureWorks2017].[Sales].[SalesTerritory] ON  [AdventureWorks2017].[Sales].[Customer].[TerritoryID] = [AdventureWorks2017].[Sales].[SalesTerritory].TerritoryID where [PersonID]  is NULL AND NOT Sales.SalesTerritory.CountryRegionCode = 'US'")
data_USA = db.get_engine(bind='mssql').execute(sql_us)
data_all = db.get_engine(bind='mssql').execute(sql_all)
data_all2 = db.get_engine(bind='mssql').execute(sql_null2)
data_USA2 = db.get_engine(bind='mssql').execute(sql_null1)

f = open('sol.txt','w')

for u in data_USA:
    f.write(str(u[1]) + ','+str(u[2])+ ','+'United States'+ ','+str(u[4])+ ','+str(u[5]) + '\n')
f.close()

f2 = open('sol.txt','a')
for a in data_all:
    f2.write(str(u[1]) + ','+str(u[2])+ ','+str(a[3])+ ','+str(u[4])+ ','+str(u[5]) + '\n')
f2.close()

f3 = open('sol.txt','a')
for x in data_USA2:
    f3.write('' + ','+''+ ','+'United States'+ ','+''+ ','+''+ '\n')
f3.close()

f4 = open('sol.txt','a')
for r in data_all2:
    f4.write('' + ','+''+ ','+str(r[1])+ ','+''+ ','+''+ '\n')
f4.close()

#para convertir utf8 para poder load mamaisela
#os.system('powershell.exe Get-Content sol2.txt -Encoding Oem ^| Out-File abel.txt -Encoding utf8')