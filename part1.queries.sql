PRAGMA FOREIGN_KEYS = ON; 
PRAGMA foreign_key_List(Orders);
PRAGMA Table_Info(customers);
PRAGMA Table_Info(orders);


--Task 2(a): where + not in
SELECT *
FROM Customers
WHERE Country NOT IN ('USA', 'Germany');

--Task 2(b): Between 
SELECT *
FROM Orders
WHERE Freight BETWEEN 100 AND 200;

--Task 2(c): ORDER BY + ASC
SELECT *
FROM Customers
ORDER BY CompanyName ASC;

--Task 2 (d): ORDER BY + DESC
SELECT *
FROM Orders
ORDER BY OrderDate DESC;

--Task 2(e): Subquery (Nested select) -customer with no Orders (not exists)
SELECT *
FROM Customers c
WHERE NOT EXISTS (SELECT 1 FROM Orders o WHERE o. CustomerID = c.CustomerID); 

--Task 2(f): like +  Wildcard
SELECT *
FROM Customers
WHERE ContactName LIKE 'A%';

SELECT name 
FROM sqlite_master 
WHERE type='table';

PRAGMA Table_Info('products');

--TASK 3(a): GROUP BY + HAVING
SELECT CategoryID,
COUNT(*) AS total_product,
AVG(UnitPrice) AS average_price
FROM Products
GROUP BY CategoryID
HAVING AVG(UnitPrice) > 20;

 --TASK 4(A): INNER JOIN
SELECT
c.CustomerID,
c.CompanyName,
o.OrderID, 
o.OrderDate
FROM Customers as c
INNER JOIN Orders as o
ON c.CustomerID = o.CustomerID;

 --TASK 4(B): LEFT JOIN
SELECT
c.CustomerID,
c.CompanyName,
o.OrderID,
o.OrderDate
FROM Customers as c
LEFT JOIN Orders as o
ON c.CustomerID = o.CustomerID;

--Task 5(a): count + distinct customer id
SELECT COUNT(DISTINCT CustomerID) AS total_customers
FROM Customers;

--Task 5 (b): check 1:1 or 1:many using Group by
SELECT CustomerID, COUNT(*) AS total_orders
FROM Orders
GROUP BY CustomerID
ORDER BY total_orders DESC;
 

--TASK 5 (c): check for orphan records
SELECT o.CustomerID
FROM Orders o
LEFT JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE c.CustomerID IS NULL;

--TASK 6 : EXPORT TASK 4(B) LEFT JOIN RESULTS TO CSV
SELECT
c.CustomerID,
c.CompanyName,
o.OrderID,
o.OrderDate
FROM Customers as c
LEFT JOIN Orders as o
ON c.CustomerID = o.CustomerID;


 