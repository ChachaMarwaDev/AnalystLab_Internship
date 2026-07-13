import duckdb

def get_connection():
    con = duckdb.connect()
    con.sql("INSTALL sqlite; LOAD sqlite")
    con.sql("ATTACH 'Chinook_Sqlite.sqlite' AS chinook (TYPE sqlite)")
    return con

def run_query(con, query:str):
    return con.sql(query).df()