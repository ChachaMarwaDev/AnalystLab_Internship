# %%
from connect import get_connection, run_query

con = get_connection()

# %%
print(run_query(con, "SHOW ALL TABLES"))

# %%
print(run_query(con, "SELECT DISTINCT country FROM chinook.Customer"))

# %%
with open("queries.sql") as f:
    print(run_query(con, f.read()))
# %%
