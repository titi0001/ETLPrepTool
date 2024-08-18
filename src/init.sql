DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'crm') THEN
      PERFORM pg_catalog.set_config('search_path', '', false);
      EXECUTE 'CREATE DATABASE crm';
   END IF;
END
$do$;

\c crm;

DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'dCliente') THEN
      CREATE TABLE dCliente (
         CustomerKey SERIAL PRIMARY KEY,  
         BusinessType VARCHAR(255),               
         StateCode VARCHAR(10),                  
         StateName VARCHAR(255),                  
         CityName VARCHAR(255),                   
         Continent VARCHAR(255),                  
         CountryName VARCHAR(255),                
         Customer VARCHAR(255)                   
      );
   END IF;
END
$do$;

DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'dProduto') THEN
      CREATE TABLE dProduto (
         CategoryName VARCHAR(100),
         ProductDetail VARCHAR(255),
         ProductKey INTEGER PRIMARY KEY, 
         ProductName VARCHAR(255),
         ProductSize VARCHAR(100),
         SubcategoryName VARCHAR(100),
         UnitPrice DECIMAL(12, 3)
      );
   END IF;
END
$do$;

DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'fVendas') THEN
      CREATE TABLE fVendas (
         CustomerKey INTEGER,              
         DueDate TIMESTAMP,                 
         OrderDate TIMESTAMP,               
         ShipDate TIMESTAMP,                
         ProductKey INTEGER,               
         SalesOrderNumber VARCHAR(50),      
         OrderQuantity INTEGER,            
         PRIMARY KEY (SalesOrderNumber, ProductKey)  
      );
   END IF;
END
$do$;

DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'fMetas') THEN
      CREATE TABLE fMetas (
         Pais VARCHAR(255),                       
         Ano INT,                     
         Meta DECIMAL(12, 3),
         PRIMARY KEY (Pais, Ano)             
      );
   END IF;
END
$do$;

ALTER TABLE fVendas
ADD CONSTRAINT fk_fvendas_customerkey
FOREIGN KEY (CustomerKey) REFERENCES dCliente (CustomerKey),
ADD CONSTRAINT fk_fvendas_productkey
FOREIGN KEY (ProductKey) REFERENCES dProduto (ProductKey);