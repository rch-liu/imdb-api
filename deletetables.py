import psycopg2
from util import get_table_names

conn = psycopg2.connect("dbname=testdb") # TODO: rename db
cur = conn.cursor()
TABLES = ", ".join(get_table_names())
cur.execute(f"DROP TABLE {TABLES}")
cur.close()
conn.commit()
conn.close()

print('Successfully deleted tables.')
