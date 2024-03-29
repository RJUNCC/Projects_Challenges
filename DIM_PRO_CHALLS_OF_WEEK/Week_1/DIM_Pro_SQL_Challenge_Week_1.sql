-- Active: 1698255203229@@127.0.0.1@3307
-- Drop the database if it already exists
DROP DATABASE IF EXISTS RetailSalesDB;

-- Create a new database named 'RetailSalesDB'
CREATE DATABASE RetailSalesDB;
USE RetailSalesDB;

-- Create the 'Products' table
CREATE TABLE Products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    Category VARCHAR(100) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL
);

-- Create the 'Sales' table
CREATE TABLE Sales (
    SaleID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    SalespersonID INT NOT NULL,
    Region VARCHAR(50) NOT NULL,
    QuantitySold INT NOT NULL,
    SaleDate DATE NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

USE RetailSalesDB;

-- Insert data into the 'Products' table
INSERT INTO Products (ProductName, Category, Price)
VALUES 
('Laptop', 'Electronics', 1000.00),
('Smartphone', 'Electronics', 700.00),
('Jeans', 'Clothing', 50.00),
('T-Shirt', 'Clothing', 20.00),
('Table', 'Furniture', 200.00),
('Chair', 'Furniture', 70.00),
('Coffee', 'Groceries', 5.00),
('Milk', 'Groceries', 1.50);

-- Insert data into the 'Sales' table
INSERT INTO Sales (ProductID, SalespersonID, Region, QuantitySold, SaleDate)
VALUES 
(1, 101, 'North', 3, '2023-01-05'),
(2, 101, 'North', 5, '2023-01-15'),
(3, 102, 'South', 10, '2023-02-01'),
(4, 102, 'South', 20, '2023-02-15'),
(5, 103, 'East', 2, '2023-03-01'),
(6, 103, 'East', 4, '2023-03-20'),
(7, 104, 'West', 50, '2023-04-01'),
(8, 104, 'West', 100, '2023-04-10'),
(1, 101, 'North', 2, '2023-05-01'),
(2, 102, 'South', 6, '2023-05-20'),
(3, 103, 'East', 15, '2023-06-05'),
(4, 104, 'West', 25, '2023-06-15'),
(5, 101, 'North', 3, '2023-07-01'),
(6, 102, 'South', 4, '2023-07-15'),
(7, 103, 'East', 60, '2023-08-01'),
(8, 104, 'West', 120, '2023-08-20');

-- Find the top 2 products with the highest sales for each month in 2023.
WITH MonthlySales AS (
    SELECT
        MONTH(SaleDate) AS SaleMonth,
        ProductID,
        SUM(QuantitySold) AS TotalQuantitySold
    FROM Sales
    WHERE YEAR(SaleDate) = 2023
    GROUP BY SaleMonth, ProductID
),
Ranking AS (
    SELECT
        SaleMonth,
        ProductID,
        TotalQuantitySold,
        RANK() OVER(PARTITION BY SaleMonth ORDER BY TotalQuantitySold DESC) AS rnk
    FROM MonthlySales
)
SELECT
    Ranking.SaleMonth,
    Products.ProductName,
    Ranking.TotalQuantitySold
FROM Ranking
JOIN Products USING(ProductID)
WHERE Ranking.rnk <= 2
ORDER BY Ranking.SaleMonth, Ranking.TotalQuantitySold DESC;

-- For each month in 2023, find the salesperson who achieved the highest sales.
WITH MonthlySales AS (
    SELECT 
        MONTH(SaleDate) AS SaleMonth,
        SalespersonID,
        SUM(QuantitySold*Products.price) AS TotalRevenue
    FROM Sales
    JOIN Products USING(ProductID)
    WHERE YEAR(SaleDate) = 2023
    GROUP BY SaleMonth, SalespersonID
),
RANKING AS (
    SELECT
        SaleMonth,
        SalespersonID,
        TotalRevenue,
        RANK() OVER(PARTITION BY SaleMonth ORDER BY TotalRevenue DESC) AS rnk
    FROM MonthlySales
)
SELECT
    Ranking.SaleMonth,
    Ranking.SalespersonID,
    Ranking.TotalRevenue
FROM Ranking
WHERE Ranking.rnk = 1;

-- Find the product that had the most significant sales increase from February to March 2023.
WITH MonthlyDifference AS (
    SELECT
        Products.ProductID,
        Products.ProductName,
        COALESCE(SUM(CASE WHEN MONTH(SaleDate) = 2 THEN Sales.QuantitySold ELSE 0 END)) AS FebruarySales,
        COALESCE(SUM(CASE WHEN MONTH(SaleDate) = 3 THEN Sales.QuantitySold ELSE 0 END)) AS MarchSales
    FROM Products
    JOIN Sales USING(ProductID)
    GROUP BY Products.ProductID, Products.ProductName
)
SELECT
    ProductID,
    ProductName,
    (MarchSales - FebruarySales) AS SalesDifference
FROM MonthlyDifference
ORDER BY SalesDifference DESC;

-- Calculate the average revenue generated per sale for each product category in 2023.
-- Create a metric called the Product Popularity Index (PPI). It is calculated as (Total Units Sold of Product) / (Total Units Sold of All Products) * 100 for 2023.
-- Considering each distinct salesperson as a “customer”, calculate an estimated CLV (Customer Lifetime Value) for each salesperson for 2023. The CLV is calculated as (Average Revenue Per Sale by Salesperson) * (Number of Sales by Salesperson).
-- Calculate the month-over-month growth rate for total sales revenue in 2023. The growth rate is calculated as ((Revenue of Current Month - Revenue of Previous Month) / Revenue of Previous Month) * 100.
-- Submission Instructions