# Written with the help from https://stackoverflow.com/a/19473206

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Open and read the file as a single bufferq
fd_metadata = open('./production_data/metadata_out.csv', 'r')
fd_films = open('./production_data/films_out.csv', 'r')
fd_ratings = open('./production_data/ratings_out.csv', 'r')
fd_names = open('./production_data/names_out.csv', 'r')
fd_crew = open('./production_data/crew_out.csv', 'r')

# Connect to the PostgreSQL server
conn = psycopg2.connect("dbname=testdb")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# Copy over all csv data for each table
cur.copy_from(fd_metadata, 'metadata', sep = '|')
fd_metadata.close()

cur.copy_from(fd_films, 'films', sep = '|')
fd_films.close()

cur.copy_from(fd_ratings, 'ratings', sep = '|')
fd_ratings.close()

cur.copy_from(fd_names, 'names', sep = '|')
fd_names.close()

cur.copy_from(fd_crew, 'crew', sep = '|')
fd_crew.close()

# Close communication with the PostgreSQL database server
cur.close()

# Commit the changes
conn.commit()
conn.close()

print('Successfully populated tables.')