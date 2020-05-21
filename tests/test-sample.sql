SELECT films.original_title, ratings.average_ratings 
FROM ratings, films
WHERE films.start_year > 1894 AND
      films.start_year < 1897 AND
      ratings.tconst = films.tconst AND
      ratings.num_votes >= 10
ORDER BY ratings.average_ratings DESC
LIMIT 10