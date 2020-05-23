# IMDB API
### Setup 
You must have PostgreSQL installed and started on your machine. To connect to PostgreSQL, execute:
```
pg_ctl -D /usr/local/var/postgres/ start
psql -d postgres
```
where `/usr/local/var/postgres` is the file system location of the database configuration files when you installed PostgreSQL.

To close the connection, execute:
```
pg_ctl -D /usr/local/var/postgres/ stop
```

Then, execute
```SQL
CREATE DATABASE testdb;
```
using whichever SQL execution method you prefer (e.g., CLI, Postico)
to create the `testdb` database.

Next, execute:
```
python api.py
```
to populate tables and expose the API on port 5000.


### Implementation
To setup the database, run
```bash
python createTables.py # initializes all empty tables
```

To populate the database with production data, run
```bash
python populateTables.py # populates empty tables with production data
```

To delete all tables, run
```bash
python deleteTables.py
```

Launching the api is still the same: `python api.py`.

To test queries without the frontend, start the api and execute
```bash
curl "127.0.0.1:5000/<endpoint>?<queries>"
```
#### Login (/login)
This endpoint attempts to authenticate a user with a given username and password.

To test authentication, run
```bash
curl "127.0.0.1:5000/login?username=foo&password=bar"
```

#### Signup (/signup)
This endpoint attempts to create a new user with given username and password.

To test signup, run
```bash
curl "127.0.0.1:5000/signup?username=foo&password=bar" -X POST
```

#### Add Favourite Film (/add_favourite)
This endpoint adds a film to a user's list of favourite films.

To test add_favourite, run
```bash
curl "127.0.0.1:5000/add_favourite?username=foo&FilmID=tt0000088" -X POST
```

#### Add Favourite Film (/remove_favourite)
This endpoint removes a film to a user's list of favourite films if it exists.

To test remove_favourite, run
```bash
curl "127.0.0.1:5000/remove_favourite?username=foo&FilmID=tt0000088" -X POST
```

#### View Favourite Films (/view_favourites)
This endpoint allows users to view their list of favourite films

To test view_favourite, run
```bash
curl "127.0.0.1:5000/view_favourites?username=foo" -X GET
```

#### View Users Statistics (/view_user_stats)
This endpoint displays to viewers a summary of statistics on user behaviour including:
* the total number of users on the application
* the top 10 favourite films chosen by users
* the average number of favourite movies by all users

To test view_user_stats, run
```bash
curl "127.0.0.1:5000/view_user_stats" -X GET
```

#### Search movies with certain parameters (/movies)
This endpoint displays all the movies' information.
* Diplays all the attributes in films table and attach it's rating as well as it's regions
* Uses either leftYear, rightYear, title, name, rating, genre and region or only tconst as parameters

Example usage: Get all the "Documentary" movies between 1984 and 1985 in "FR" region, run
```bash
curl "127.0.0.1:5000/movies?leftYear=1894&rightYear=1895&genre=Documentary
            &region=BR&title=STARWARS&name=Akiva&rating=9"
```
Example usage: Get the movie with tconst = tt0000005
```bash
curl "127.0.0.1:5000/movies?tconst=tt0000005"
```


#### View all the unique regions in database (/regions)
This endpoint displays all the unique region entries in our database.

To test regions, run
```bash
curl "127.0.0.1:5000/regions"
```

#### View all the unique genres in database (/genres)
This endpoint displays all the unique genre entries in our database.

To test genres, run
```bash
curl "127.0.0.1:5000/genres"
```

#### Find Matches (/find_matches)
This endpoint matches a user with another user based on favourite films

To test find_matches, run
```bash
curl "127.0.0.1:5000/find_matches" -X POST
```

#### Submit Rating (/submit_rating)
This endpoint allows a user to submit their rating of a film

To test submit_rating, run
```bash
curl "127.0.0.1:5000/submit_rating" -X POST
```

#### Names (/names)
This endpoint fetches all the names of cast and crew who worked on a specific film

To test names, run
```bash
curl "127.0.0.1:5000/names" -X GET
```

#### Regions (/regions)
This endpoint retrieves all possible regions of films from the IMDB database

To test names, run
```bash
curl "127.0.0.1:5000/regions" -X GET
```

#### Genres (/genres)
This endpoint retrieves all possible genres of films from the IMDB database

To test names, run
```bash
curl "127.0.0.1:5000/genres" -X GET
```

### Note: All endpoints and queries are located in api.py
