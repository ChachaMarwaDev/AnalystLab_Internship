# %%
import duckdb

# Install and load the sqlite extension (only needed once)
# I have run it so I will comment it out
# duckdb.sql("INSTALL sqlite; LOAD sqlite;")

# %%
# Attach the Chinook database
duckdb.sql("ATTACH 'Chinook_Sqlite.sqlite' AS chinook (TYPE sqlite)")

# Test it - list all tables
print(duckdb.sql("SHOW ALL TABLES").df())

# %%
# Test
result = duckdb.sql("""
    SELECT * FROM chinook.Customer LIMIT 5
""").df()
print(result)
# %%
