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
# Checing distinct columns in country
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