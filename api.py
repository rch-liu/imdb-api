from flask import Flask, g, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from user.user import User
import psycopg2
import json

# Reveal API
app = Flask(__name__)
app.config["DEBUG"] = True

cur = None
conn = None

@app.before_request
def before_request():
  conn = psycopg2.connect("dbname=testdb")
  conn.autocommit = True
  # Establish the conn variable as global so it persists throughout multiple requests
  g.db = conn

@app.route('/view_user_stats', methods=['GET'])
def view_user_stats():
  cur = g.db.cursor()

  # Gets the total number of users on the application
  cur.execute("SELECT COUNT(*) FROM users;")
  res_user = cur.fetchall()[0][0]
  print(res_user)

  # Gets the top 10 favourite films by users
  cur.execute("SELECT primary_title, CAST(ROUND(r.average_ratings, 2)AS varchar(20)), m.tconst, is_adult, start_year, runtime_minutes, genres FROM films m JOIN (SELECT tconst, average_ratings, COUNT(tconst) FROM ratings GROUP BY tconst) AS r ON m.tconst = r.tconst LIMIT 10;")
  res_top = [
    {
      "title": i[0],
      "rating": i[1],
      "tconst": i[2],
      "is_adult": i[3],
      "start_year": i[4],
      "runtime_minutes": i[5],
      "genres": i[6].split(","),
    } for i in cur.fetchall()]
  print(res_top)

  # Gets the average number of favourite movies by all users
  cur.execute("SELECT CAST(ROUND(AVG(NUM_FILMS),2) AS varchar(20)) AS AVG_NUM_FILMS FROM (SELECT COUNT(tconst) AS NUM_FILMS FROM favouriteFilms GROUP BY USER_ID) AS A;")
  res_avg = cur.fetchall()[0][0]
  print(res_avg)

  return jsonify({
    'total_users': res_user,
    'top_10_films': res_top,
    'average_favourites': res_avg
  })


@app.route('/movies', methods=['GET'])
def movies():
  tconst = request.args.get('tconst') or ""
  leftYear = request.args.get('leftYear')
  rightYear = request.args.get('rightYear')
  title = request.args.get('title') or ""
  name = request.args.get('name') or ""
  rating = 0 if (request.args.get('rating') == None or request.args.get('rating') == "") else int(request.args.get('rating'))
  genre = request.args.get('genre') or ""
  region = request.args.get('region') or ""
  cur = g.db.cursor()
  json_res = []

  #tconst is given
  if tconst != "":

    #Get movie attributes
    cur.execute(f"""
    SELECT *
    FROM films
    WHERE tconst = '{tconst}';
    """)
    res = cur.fetchone()

    #Add it's rating
    cur.execute(f"""
    SELECT average_ratings
    FROM ratings
    WHERE tconst = '{tconst}';
    """)
    temp_rating = cur.fetchone()
    
    #Append region list to the end of the tuples
    cur.execute(f"""
    SELECT DISTINCT region 
    FROM metadata 
    WHERE title_id = '{tconst}' AND region IS NOT NULL;
    """)
    temp_region = cur.fetchall()
    #Create a string array of regions
    regions = []
    for reg in temp_region:
      regions.append(reg[0])

    #Append each member of crew with their role as a list to the end of the tuples
    cur.execute(f"""
    SELECT category, primary_name 
    FROM crew, names
    WHERE tconst = '{tconst}' AND crew.nconst = names.nconst;
    """)
    temp_names = cur.fetchall()
    #Create a string array of regions
    names = []
    for current in temp_names:
      dict_names= {}
      dict_names['name'] = current[1]
      dict_names['role'] = current[0]
      names.append(dict_names)

    #Turn everything into json format with dictionary
    dict_film = {}
    dict_film['tconst'] = res[0]
    dict_film['title_type'] = res[1]
    dict_film['title'] = res[2]
    dict_film['original_title'] = res[3]
    dict_film['is_adult'] = res[4]
    dict_film['start_year'] = res[5]
    dict_film['runtime_minutes'] = res[6]
    #Convert mixed string style of genres into array of string
    dict_film['genres'] = res[7].split(",")
    dict_film['average_ratings'] = float(temp_rating[0])
    dict_film['region'] = regions
    dict_film['names'] = names
    json_res.append(dict_film)
  
  # tconst is not given
  else:
    # Only films table needed
    tables = "films"
    condition = f"""
    start_year >= CAST('{leftYear}' AS INTEGER) AND
    start_year <= CAST('{rightYear}' AS INTEGER) AND
    CASE WHEN '{title}' = '' THEN TRUE ELSE LOWER(primary_title) LIKE CONCAT('%', LOWER('{title}'), '%') END AND
    CASE WHEN '{genre}' = '' THEN TRUE ELSE genres LIKE CONCAT('%', '{genre}', '%') END
    """

    if rating != 0: 
      tables += ", ratings"
      condition += f""" AND average_ratings >= '{rating}' AND films.tconst = ratings.tconst"""
    if name != '':
      tables += ", names"
      condition += f""" AND known_for_titles LIKE CONCAT('%', films.tconst, '%') AND LOWER(primary_name) LIKE CONCAT('%', LOWER('{name}'), '%')"""
    if region != '':
      tables += ", metadata"
      condition += f""" AND region = '{region}' AND films.tconst = title_id"""

    cur.execute(f"""
    SELECT DISTINCT films.tconst, primary_title, is_adult, start_year, runtime_minutes, genres
    FROM {tables}
    WHERE {condition};
    """)
    res = cur.fetchall()

    for record in res:
      #Turn everything into json format with dictionary
      dict_film = {}
      dict_film['tconst'] = record[0]
      dict_film['title'] = record[1]
      dict_film['is_adult'] = record[2]
      dict_film['start_year'] = record[3]
      dict_film['runtime_minutes'] = record[4]
      #Convert mixed string style of genres into array of string
      dict_film['genres'] = record[5].split(",")
      json_res.append(dict_film)

  return json.dumps(json_res)


@app.route('/regions', methods=['GET'])
def regions():
  #This function returns all the possible regions in our data
  cur = g.db.cursor()
  cur.execute("""
  SELECT DISTINCT region 
  FROM metadata 
  WHERE region IS NOT NULL 
  ORDER BY region;
  """)
  res = cur.fetchall()

  #list of lists -> list of strings
  output = []
  for region in res:
    output.append(region[0])

  return json.dumps(output)


@app.route('/genres', methods=['GET'])
def genres():
  #This function returns all the possible genres in our data
  cur = g.db.cursor()
  cur.execute("""
  SELECT DISTINCT genres 
  FROM films 
  WHERE genres IS NOT NULL 
  ORDER BY genres;
  """)
  res = cur.fetchall()

  #list of lists -> list of strings
  output = set()
  for genre in res:
    for word in genre[0].split(","):
      if word not in output: output.add(word)

  return json.dumps(list(output))


@app.route('/names', methods=['GET'])
def names():
  cur = g.db.cursor()
  tconst = request.args.get('FilmID')
  # Cap it at 1000 or take too long hitting the endpoint
  cur.execute(f"SELECT * FROM names WHERE known_for_titles LIKE ('%{tconst}%') LIMIT 1000;")
  # res = cur.fetchall()
  res = [{
    "known_for_titles":i[5],
    "primary_profession": i[4],
    "death_year": i[3],
    "birth_year": i[2], 
    "primary_name": i[1], 
    "nconst": i[0]} for i in cur.fetchall()]
  return json.dumps(res)

@app.route('/login', methods=['GET'])
def login():
  """
  Accepts query parameters:
    - username (the user's username)
    - password (the user's attempt at their password)
  """
  usr = request.args.get('username')
  pswrd = request.args.get('password')
  res = User.find_by_username(usr)

  userResponse = None
  status = -1 # initially set to: user does not exist
  if res is not None:
    if not User.validate_password(pswrd, res[1]):
      status = 1 # user exists but password is incorrect
    else:
      userResponse = usr
      status = 10 # user exists and password is correct
  
  return jsonify({
    'user': userResponse, # return the username to the frontend to be stored in localStorage
    'status': status
  })

@app.route('/view_favourites', methods=['GET'])
def view_favourites():
    usr = request.args.get('username')
    cur = g.db.cursor()
    cur.execute(f"SELECT primary_title, CAST(ROUND(average_ratings, 2)AS varchar(20)), films.tconst, is_adult, start_year, runtime_minutes, genres  FROM favouriteFilms, films, ratings WHERE user_id = ('{usr}') AND favouriteFilms.tconst = films.tconst AND films.tconst = ratings.tconst;")
    res_top = [
      {
        "title": i[0],
        "rating": i[1],
        "tconst": i[2],
        "is_adult": i[3],
        "start_year": i[4],
        "runtime_minutes": i[5],
        "genres": i[6].split(","),
      } for i in cur.fetchall()]
    return json.dumps(res_top)

@app.route('/add_favourite', methods=['POST'])
def add_favourite():
  usr = request.args.get('username')
  res = User.find_by_username(usr)
  status = 500
  if res is not None:
    status = 200
    tconst = request.args.get('FilmID')
    cur = g.db.cursor()
    cur.execute(f"INSERT INTO favouriteFilms(user_id, tconst) VALUES ('{usr}','{tconst}');")
    return jsonify({
      'exit_code': status
    })
  return jsonify({
    'exit_code': status
  })

@app.route('/remove_favourite', methods=['POST'])
def remove_favourite():
  usr = request.args.get('username')
  res = User.find_by_username(usr)
  status = 500
  if res is not None:
    status = 200
    tconst = request.args.get('FilmID')
    cur = g.db.cursor()
    cur.execute(f"DELETE FROM favouriteFilms WHERE tconst='{tconst}' AND user_id='{usr}';")
    return jsonify({
      'exit_code': status
    })
  return jsonify({
    'exit_code': status
  })

@app.route('/find_matches', methods=['GET'])
def find_matches():
  usr = request.args.get('username')
  res = User.find_by_username(usr)
  status = 500
  if res is not None:   
    cur = g.db.cursor()
    cur.execute(f"""
      CREATE OR REPLACE VIEW view1 AS 
        SELECT user_id, tconst from favouriteFilms 
        WHERE tconst IN (SELECT tconst FROM favouriteFilms WHERE user_id = '{usr}') 
          AND user_id <> '{usr}'
        ORDER BY user_id
        LIMIT 1000;
        
        SELECT user_id, list FROM (
          SELECT user_id, array_to_string(ARRAY_AGG(primary_title), ',') as list, COUNT(primary_title) 
          FROM (SELECT user_id, primary_title from view1 INNER JOIN films ON view1.tconst = films.tconst) as x
        GROUP BY user_id
        ORDER BY COUNT(primary_title) DESC
        LIMIT 10) as y;
      """)
    res = [{"user": i[0], "movies": i[1].split(",")} for i in cur.fetchall()]
    return json.dumps(res)
  return jsonify({
    'exit_code': status
  })

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
  usr = request.args.get('username')
  res = User.find_by_username(usr)
  status = 400 # username not found
  if res is not None:
    tconst = request.args.get('FilmID')
    rating = int(request.args.get('Rating'))
    if 0 <= rating <= 10:
      status = 350
      cur = g.db.cursor()
      cur.execute(f"SELECT average_ratings FROM ratings WHERE tconst = '{tconst}';")
      old_rating = float(cur.fetchone()[0])
      cur.execute(f"SELECT num_votes FROM ratings WHERE tconst = '{tconst}';")
      num_votes = int(cur.fetchone()[0])
      new_rating = (((old_rating * num_votes) + rating)) / (num_votes + 1)
      num_votes += 1
      cur.execute(f"UPDATE ratings SET average_ratings = '{new_rating}', num_votes = '{num_votes}' WHERE tconst = '{tconst}';")
      return jsonify({
        'exit_code': status
      })
    else:
      status = 300 # rating not between 0 and 10
  return jsonify({
    'exit_code': status
  })


@app.route("/signup", methods=["POST"])
def signup():
  # Get user input
  usr = request.args.get('username')
  pswrd = request.args.get('password')

  # Check for blanks
  if usr == "" or pswrd == "":
    status = -2 # Empty input
  else:
    res = User.find_by_username(usr)
    status = 2 # Username is already exist
    if res is None:
      newUser = User(usr, pswrd)
      newUser.save_to_db()
      status = 11 # Username does not exist thus can be used

  return jsonify({
  'status': status
})

@app.after_request
def after_request(response):
  if g.db is not None:
      print('closing connection')
      g.db.close()
  if cur is not None:
      print('closing cursor')
      cur.close()
      
  return response

app.run()
