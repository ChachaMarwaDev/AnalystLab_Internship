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
with open("queries.sql") as f:
    content = f.read()

# Split the file into individual statements on ';'
# and drop empty pieces or ones that are only comments
raw_statements = content.split(';')

statements = []
for s in raw_statements:
    s = s.strip()
    if not s:
        continue
    # remove comment-only lines so we don't try to "run" a pure comment block
    lines = [line for line in s.split('\n') if not line.strip().startswith('--')]
    cleaned = '\n'.join(lines).strip()
    if cleaned:
        statements.append(cleaned)

print(f"Found {len(statements)} statements to run\n")

for i, stmt in enumerate(statements, start=1):
    print(f"\n{'='*60}")
    print(f"Statement {i}:")
    print(stmt[:100] + ("..." if len(stmt) > 100 else ""))
    print('='*60)
    try:
        result = run_query(con, stmt)
        print(result)
    except Exception as e:
        print(f"ERROR: {e}")
# %%
