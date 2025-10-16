-- Create a database named "FOTOFOLIO"
CREATE DATABASE FOTOFOLIO;

-- Use the "FOTOFOLIO" database
USE FOTOFOLIO;
GO

-- Check if there are any existing records in the "transactions" table
SELECT *
FROM transactions;

-- Delete the “transactions” table because 
-- I want to fill it with csv data with 
-- the latest format and content. 
DROP TABLE transactions;


-- Create a new "transactions" table with specific columns
CREATE TABLE transactions (
    InvoiceNo VARCHAR(20),
    StockCode VARCHAR(20),
    Description VARCHAR(255),
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice DECIMAL(10, 2),
    CustomerID INT,
    Country VARCHAR(50)
);

-- Bulk insert data into the "transactions" table from a CSV file
-- This process can actually be done without a query, but this time I used a query
-- because I wanted to show off my skills in using traditional SQL methods. 
-- The method without a query is :
-- right-click on the database -> tasks -> select the import method. 
-- Personally, I prefer the flat import method because it is simpler.

BULK INSERT transactions
FROM "(Changed for privacy reasons, this is basically my local .csv file path)"
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
GO

-- Checking The Code
-- Select all records from the "transactions" table
SELECT *
FROM transactions;

-- Calculate the total revenue by country
SELECT TOP 10 Country, ROUND(SUM(Quantity * UnitPrice), 2) AS total_revenue
FROM transactions
WHERE Quantity > 0 AND UnitPrice > 0
GROUP BY Country
ORDER BY total_revenue DESC;

-- Calculate the total spending by customer
SELECT TOP 10 CustomerID, ROUND(SUM(Quantity * UnitPrice), 2) AS total_spending
FROM transactions
WHERE CustomerID IS NOT NULL AND Quantity > 0 AND UnitPrice > 0
GROUP BY CustomerID
ORDER BY total_spending DESC;