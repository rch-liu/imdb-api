import csv

infile = open("production_data/films.csv", "r")
outfile = open("production_data/films_out.csv", "w")

csvReader = csv.reader(infile)

for line in csvReader:
    outfile.write("|".join(line) + "\n")

infile = open("production_data/ratings.csv", "r")
outfile = open("production_data/ratings_out.csv", "w")

csvReader = csv.reader(infile)

for line in csvReader:
    outfile.write("|".join(line) + "\n")

infile = open("production_data/metadata.csv", "r")
outfile = open("production_data/metadata_out.csv", "w")

csvReader = csv.reader(infile)

for line in csvReader:
    outfile.write("|".join(line) + "\n")

infile.close()
outfile.close()

infile = open("production_data/names.csv", "r")
outfile = open("production_data/names_out.csv", "w")

csvReader = csv.reader(infile)

for line in csvReader:
    outfile.write("|".join(line) + "\n")

infile.close()
outfile.close()

infile = open("production_data/crew.csv", "r")
outfile = open("production_data/crew_out.csv", "w")

csvReader = csv.reader(infile)

for line in csvReader:
    outfile.write("|".join(line) + "\n")

infile.close()
outfile.close()