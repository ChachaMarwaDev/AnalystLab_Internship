-- SELECT + WHERE: cancelled orders
SELECT ORDERNUMBER, CUSTOMERNAME, STATUS, SALES FROM sales WHERE STATUS = 'Cancelled';

-- ORDER BY: highest value orders
SELECT ORDERNUMBER, CUSTOMERNAME, SALES
FROM sales
ORDER BY SALES DESC
LIMIT 10;

-- GROUP BY + aggregate: total sales per country
SELECT COUNTRY, SUM(SALES) AS total_sales
FROM sales
GROUP BY COUNTRY
ORDER BY total_sales DESC;

-- HAVING: countries with over $500,000 in total sales
SELECT COUNTRY, SUM(SALES) AS total_sales
FROM sales
GROUP BY COUNTRY
HAVING SUM(SALES) > 500000
ORDER BY total_sales DESC;

-- Aggregate functions together: product line performance
SELECT 
    PRODUCTLINE,
    COUNT(*) AS num_orders,
    SUM(SALES) AS total_sales,
    AVG(SALES) AS avg_sale,
    SUM(QUANTITYORDERED) AS total_units
FROM sales
GROUP BY PRODUCTLINE
ORDER BY total_sales DESC;

-- Self-join: compare each order to other orders from the same customer
SELECT 
    a.ORDERNUMBER AS order_1,
    b.ORDERNUMBER AS order_2,
    a.CUSTOMERNAME,
    a.SALES AS sales_1,
    b.SALES AS sales_2
FROM sales a
INNER JOIN sales b 
    ON a.CUSTOMERNAME = b.CUSTOMERNAME 
    AND a.ORDERNUMBER < b.ORDERNUMBER
LIMIT 10;

-- Orders above the average sale amount
SELECT ORDERNUMBER, CUSTOMERNAME, SALES
FROM sales
WHERE SALES > (SELECT AVG(SALES) FROM sales)
ORDER BY SALES DESC;

-- Customers whose total spend is in the top 10%
SELECT CUSTOMERNAME, SUM(SALES) AS total_spent
FROM sales
GROUP BY CUSTOMERNAME
HAVING SUM(SALES) > (
    SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY total)
    FROM (SELECT SUM(SALES) AS total FROM sales GROUP BY CUSTOMERNAME) t
)
ORDER BY total_spent DESC;

-- Top-performing products (by product line, since there's no single product name)
SELECT 
    PRODUCTLINE,
    SUM(SALES) AS total_revenue,
    SUM(QUANTITYORDERED) AS units_sold
FROM sales
GROUP BY PRODUCTLINE
ORDER BY total_revenue DESC;

-- Top customers
SELECT 
    CUSTOMERNAME,
    SUM(SALES) AS total_spent,
    COUNT(DISTINCT ORDERNUMBER) AS num_orders
FROM sales
GROUP BY CUSTOMERNAME
ORDER BY total_spent DESC
LIMIT 10;

-- Revenue trends over time (using pre-built YEAR_ID/MONTH_ID)
SELECT 
    YEAR_ID,
    MONTH_ID,
    SUM(SALES) AS monthly_revenue,
    COUNT(DISTINCT ORDERNUMBER) AS num_orders
FROM sales
GROUP BY YEAR_ID, MONTH_ID
ORDER BY YEAR_ID, MONTH_ID;

-- Customer purchasing behavior: average order value + deal size distribution
SELECT 
    DEALSIZE,
    COUNT(*) AS num_orders,
    AVG(SALES) AS avg_sale
FROM sales
GROUP BY DEALSIZE
ORDER BY avg_sale DESC;

-- Before indexing
EXPLAIN ANALYZE 
SELECT * FROM sales WHERE CUSTOMERNAME = 'Land of Toys Inc.';

-- Add index
CREATE INDEX idx_sales_customername ON sales(CUSTOMERNAME);

-- After indexing — compare Seq Scan vs Index Scan in the output
EXPLAIN ANALYZE 
SELECT * FROM sales WHERE CUSTOMERNAME = 'Land of Toys Inc.';

-- A second useful index for the date-based queries
CREATE INDEX idx_sales_yearmonth ON sales(YEAR_ID, MONTH_ID);