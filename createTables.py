# Written with the help from https://stackoverflow.com/a/19473206

import psycopg2

# Open and read the file as a single buffer
fd = open('createTables.sql', 'r')
sqlFile = fd.read()
fd.close()

# Connect to the PostgreSQL server
conn = psycopg2.connect("dbname=testdb")
cur = conn.cursor()

# Execute every command from the input file
cur.execute(sqlFile)

# Close communication with the PostgreSQL database server
cur.close()
# Commit the changes
conn.commit()
conn.close()

print('Successfully created tables.')
