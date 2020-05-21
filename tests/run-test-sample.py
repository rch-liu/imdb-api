import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Open and read the file as a single bufferq
fd = open('test-sample.sql', 'r')
sqlFile = fd.read()
fd.close()

# All SQL commands (split on ';')
sqlCommands = sqlFile.split(';')

# Connect to the PostgreSQL server
conn = psycopg2.connect("dbname=testdb")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# Execute every command from the input file
for command in sqlCommands:
  try:
    cur.execute(command)
  except (Exception, psycopg2.DatabaseError) as error:
    print('Error: ', error)

query = cur.fetchall() 

print("Output for test query:")
for row in query:
    print(row)

# Close communication with the PostgreSQL database server
cur.close()
# Commit the changes
conn.commit()
conn.close()

print('Successfully created tables.')
