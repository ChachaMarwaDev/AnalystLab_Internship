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
result = duckdb.sql("""
    SELECT * FROM chinook.Customer LIMIT 5
""").df()
print(result)

# %%

"""database schema           name  \
0   chinook   main          Album   
1   chinook   main         Artist   
2   chinook   main       Customer   
3   chinook   main       Employee   
4   chinook   main          Genre   
5   chinook   main        Invoice   
6   chinook   main    InvoiceLine   
7   chinook   main      MediaType   
8   chinook   main       Playlist   
9   chinook   main  PlaylistTrack   
10  chinook   main          Track"""

print(duckdb.sql("DESCRIBE chinook.Track").df())
# %%
