-- ============================================
-- CHINOOK DATABASE - SQL ANALYSIS
-- ============================================


-- ============================================
-- 2. CORE SQL QUERIES
-- ============================================

-- Distinct countries in Customer table
SELECT DISTINCT Country 
FROM Customer;

-- WHERE: customers in Poland
SELECT Company, City, Address
FROM Customer
WHERE Country = 'Poland';

-- ORDER BY: customers sorted by country
SELECT FirstName, LastName, Country
FROM Customer
ORDER BY Country
LIMIT 5;

-- GROUP BY + aggregate: number of customers per country
SELECT Country, COUNT(*) AS num_customers
FROM Customer
GROUP BY Country
ORDER BY num_customers DESC;

-- HAVING: countries with more than 5 customers
SELECT Country, COUNT(*) AS num_customers
FROM Customer
GROUP BY Country
HAVING COUNT(*) > 5;


-- ============================================
-- 3. ADVANCED SQL CONCEPTS - Joins
-- ============================================

-- INNER JOIN: revenue per track
SELECT 
    t.Name,
    SUM(il.UnitPrice * il.Quantity) AS revenue
FROM InvoiceLine il
JOIN Track t ON il.TrackId = t.TrackId
GROUP BY t.Name
ORDER BY revenue DESC
LIMIT 10;

-- LEFT JOIN: every customer, with invoices if they exist
SELECT 
    c.CustomerId, 
    c.FirstName, 
    c.LastName, 
    i.InvoiceId, 
    i.Total
FROM Customer c
LEFT JOIN Invoice i ON c.CustomerId = i.CustomerId
ORDER BY c.CustomerId
LIMIT 5;

-- RIGHT JOIN: every customer, invoices sorted by highest total
SELECT 
    c.CustomerId, 
    c.FirstName, 
    i.InvoiceId, 
    i.Total
FROM Invoice i
RIGHT JOIN Customer c ON i.CustomerId = c.CustomerId
ORDER BY i.Total DESC
LIMIT 5;


-- ============================================
-- 3. ADVANCED SQL CONCEPTS - Subqueries
-- ============================================

-- Subquery in WHERE: customers who spent above the average total
SELECT CustomerId, FirstName, LastName
FROM Customer
WHERE CustomerId IN (
    SELECT CustomerId
    FROM Invoice
    GROUP BY CustomerId
    HAVING SUM(Total) > (SELECT AVG(Total) FROM Invoice)
)
ORDER BY CustomerId;

-- Subquery in FROM: tracks priced above their album's average track price
SELECT AlbumId, Name, UnitPrice
FROM (
    SELECT 
        t.AlbumId,
        t.Name,
        t.UnitPrice,
        AVG(t.UnitPrice) OVER (PARTITION BY t.AlbumId) AS album_avg_price
    FROM Track t
) sub
WHERE UnitPrice > album_avg_price
LIMIT 10;

-- Scalar subquery: each customer's spend vs the overall average
SELECT 
    CustomerId,
    SUM(Total) AS total_spent,
    (SELECT AVG(Total) FROM Invoice) AS overall_avg_invoice
FROM Invoice
GROUP BY CustomerId
ORDER BY total_spent DESC
LIMIT 10;


-- ============================================
-- 3. ADVANCED SQL CONCEPTS - Window Functions
-- ============================================

-- RANK(): customers ranked globally by total spend
SELECT 
    CustomerId, 
    SUM(Total) AS total_spent,
    RANK() OVER (ORDER BY SUM(Total) DESC) AS spend_rank
FROM Invoice
GROUP BY CustomerId
LIMIT 5;

-- ROW_NUMBER() + PARTITION BY: rank each customer's own invoices by size
SELECT 
    CustomerId,
    InvoiceId,
    Total,
    ROW_NUMBER() OVER (PARTITION BY CustomerId ORDER BY Total DESC) AS invoice_rank
FROM Invoice
ORDER BY CustomerId, invoice_rank
LIMIT 15;

-- RANK() + PARTITION BY: top 3 tracks by revenue, within each genre
SELECT 
    g.Name AS genre,
    t.Name AS track_name,
    SUM(il.UnitPrice * il.Quantity) AS track_revenue,
    RANK() OVER (PARTITION BY g.Name ORDER BY SUM(il.UnitPrice * il.Quantity) DESC) AS genre_rank
FROM InvoiceLine il
JOIN Track t ON il.TrackId = t.TrackId
JOIN Genre g ON t.GenreId = g.GenreId
GROUP BY g.Name, t.Name
QUALIFY genre_rank <= 3
ORDER BY genre, genre_rank;

-- DENSE_RANK(): global customer ranking by total spend
SELECT 
    CustomerId,
    SUM(Total) AS total_spent,
    DENSE_RANK() OVER (ORDER BY SUM(Total) DESC) AS spend_rank
FROM Invoice
GROUP BY CustomerId
ORDER BY spend_rank
LIMIT 10;


-- ============================================
-- 4. BUSINESS PROBLEM SOLVING
-- ============================================

-- Top-performing products (tracks) by revenue
SELECT 
    t.Name AS track_name,
    SUM(il.UnitPrice * il.Quantity) AS total_revenue,
    SUM(il.Quantity) AS units_sold
FROM InvoiceLine il
JOIN Track t ON il.TrackId = t.TrackId
GROUP BY t.Name
ORDER BY total_revenue DESC
LIMIT 10;

-- Top customers by total spend
SELECT 
    c.CustomerId,
    c.FirstName || ' ' || c.LastName AS customer_name,
    SUM(i.Total) AS total_spent,
    COUNT(DISTINCT i.InvoiceId) AS number_of_orders
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId, customer_name
ORDER BY total_spent DESC
LIMIT 10;

-- Revenue trends over time (monthly)
SELECT 
    DATE_TRUNC('month', InvoiceDate) AS month,
    SUM(Total) AS monthly_revenue,
    COUNT(DISTINCT InvoiceId) AS num_invoices
FROM Invoice
GROUP BY month
ORDER BY month;

-- Revenue trends: month-over-month growth %
SELECT 
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month)) 
        / LAG(monthly_revenue) OVER (ORDER BY month) * 100, 2
    ) AS pct_growth
FROM (
    SELECT DATE_TRUNC('month', InvoiceDate) AS month, SUM(Total) AS monthly_revenue
    FROM Invoice
    GROUP BY month
) monthly;

-- Customer purchasing behavior: average order value
SELECT 
    c.CustomerId,
    c.FirstName || ' ' || c.LastName AS customer_name,
    AVG(i.Total) AS avg_order_value,
    COUNT(i.InvoiceId) AS total_orders
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId, customer_name
ORDER BY avg_order_value DESC;

-- Customer purchasing behavior: genre preference per customer
SELECT 
    c.CustomerId,
    c.FirstName || ' ' || c.LastName AS customer_name,
    g.Name AS genre,
    COUNT(*) AS tracks_bought
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
JOIN Track t ON il.TrackId = t.TrackId
JOIN Genre g ON t.GenreId = g.GenreId
GROUP BY c.CustomerId, customer_name, g.Name
ORDER BY c.CustomerId, tracks_bought DESC;

-- Customer purchasing behavior: repeat vs one-time customers
SELECT 
    CASE WHEN order_count = 1 THEN 'One-time' ELSE 'Repeat' END AS customer_type,
    COUNT(*) AS num_customers
FROM (
    SELECT CustomerId, COUNT(InvoiceId) AS order_count
    FROM Invoice
    GROUP BY CustomerId
) sub
GROUP BY customer_type;


-- ============================================
-- 5. QUERY OPTIMIZATION - Indexing Concepts
-- ============================================

-- NOTE: DuckDB is a columnar, in-process OLAP engine. It automatically
-- optimizes scans using column statistics (zone maps) and does not require
-- manual indexes the way row-store databases like Postgres/MySQL do.
-- The CREATE INDEX statements below show how this would be optimized in a
-- traditional row-store database -- this is the concept being demonstrated.

-- Without an index, this WHERE filter scans every row in Invoice (full table scan)
EXPLAIN SELECT * FROM Invoice WHERE CustomerId = 5;

-- In Postgres/MySQL, you'd speed this up with:
-- CREATE INDEX idx_invoice_customerid ON Invoice(CustomerId);
-- CREATE INDEX idx_invoiceline_trackid ON InvoiceLine(TrackId);
-- CREATE INDEX idx_invoiceline_invoiceid ON InvoiceLine(InvoiceId);
-- CREATE INDEX idx_invoice_date ON Invoice(InvoiceDate);
--
-- Why these columns: they are the ones most frequently used in JOIN ... ON
-- and WHERE clauses throughout this file (CustomerId, TrackId, InvoiceId,
-- InvoiceDate). Indexing a column lets the database jump directly to
-- matching rows instead of scanning the whole table -- similar to using
-- the index at the back of a textbook instead of reading every page.
--
-- Trade-off: indexes speed up SELECT/JOIN/WHERE but slow down
-- INSERT/UPDATE, since the index must be updated every time the underlying
-- data changes. So you index columns that are read/filtered often relative
-- to how often they're written to.

-- EXPLAIN ANALYZE: shows the actual query plan DuckDB chooses
EXPLAIN ANALYZE 
SELECT c.CustomerId, SUM(i.Total) AS total_spent
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId
ORDER BY total_spent DESC
LIMIT 10;