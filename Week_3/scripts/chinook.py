# %%
import duckdb

# Install and load the sqlite extension (only needed once)
# I have run it so I will comment it out
# duckdb.sql("INSTALL sqlite; LOAD sqlite;")

# %%
# Attach the Chinook database
# duckdb.sql("ATTACH 'Chinook_Sqlite.sqlite' AS chinook (TYPE sqlite)")

# Test it - list all tables
print(duckdb.sql("SHOW ALL TABLES").df())

# %%
# Test
# result = duckdb.sql("""
#     SELECT * FROM chinook.Customer LIMIT 5
# """).df()
# print(result)

# %%
# Describes gives you a overview of the column
# print(duckdb.sql("DESCRIBE chinook.Track").df())

# %%
# Checking distinct columns in country
print(duckdb.sql("SELECT DISTINCT(country) FROM chinook.Customer").df())

# %%
# Test check customers in Poland
print(duckdb.sql("""
    SELECT Company, City, Address
    FROM chinook.Customer
    WHERE Country='Poland'
    """).df())

# %%
# ORDER BY
print(duckdb.sql("SELECT FirstName, LastName, Country FROM chinook.Customer ORDER BY Country LIMIT 5").df())

# %%
# GROUP BY + aggregate
print(duckdb.sql("SELECT Country, COUNT(*) AS num_customers FROM chinook.Customer GROUP BY Country ORDER BY num_customers DESC").df())

# %%
# HAVING (filtering on the aggregate result)
print(duckdb.sql("SELECT Country, COUNT(*) AS num_customers FROM chinook.Customer GROUP BY Country HAVING COUNT(*) > 5").df())

# %%
# INNER JOIN: revenue per track
print(duckdb.sql("SELECT t.Name, SUM(il.UnitPrice * il.Quantity) AS revenue FROM chinook.InvoiceLine il JOIN chinook.Track t ON il.TrackId = t.TrackId GROUP BY t.Name ORDER BY revenue DESC LIMIT 10").df())

# %%
# LEFT JOIN every customer
print(duckdb.sql("""
SELECT c.CustomerId, c.FirstName, c.LastName, i.InvoiceId, i.Total FROM chinook.Customer c LEFT JOIN chinook.Invoice i ON c.CustomerId = i.CustomerId ORDER BY c.CustomerId LIMIT 5
""").df())

# %%
# RIGHT JOIN
print(duckdb.sql("""
SELECT c.CustomerId, c.FirstName, i.InvoiceId, i.Total FROM chinook.Invoice i RIGHT JOIN chinook.Customer c ON i.CustomerId = c.CustomerId ORDER BY i.total DESC LIMIT 5
""").df())

# %%
# Rank customers by total spend
print(duckdb.sql("""SELECT CustomerId, SUM(Total) AS total_spent,
RANK() OVER (ORDER BY SUM(Total) DESC) AS spend_rank FROM chinook.Invoice GROUP BY CustomerId LIMIT 5""").df())

# %%
# 