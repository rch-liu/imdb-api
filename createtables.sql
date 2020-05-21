CREATE TABLE metadata (
    title_id TEXT,
    ordering INTEGER,
    title TEXT,
    region TEXT,
    language TEXT,
    types TEXT,
    attributes TEXT,
    is_original_title BOOLEAN,
    PRIMARY KEY(title_id, ordering)
);

CREATE TABLE films (
    tconst TEXT NOT NULL PRIMARY KEY,
    title_type TEXT,
    primary_title TEXT,
    original_title TEXT,
    is_adult BOOLEAN,
    start_year INTEGER,
    runtime_minutes INTEGER,
    genres TEXT
);

CREATE TABLE ratings (
    tconst TEXT NOT NULL PRIMARY KEY,
    average_ratings NUMERIC(3,1),
    num_votes INTEGER
);

CREATE TABLE users (
    user_id VARCHAR(32),
    password VARCHAR(256),
    PRIMARY KEY(user_id)
);

CREATE TABLE favouriteFilms(
    user_id VARCHAR(32) NOT NULL,
    tconst TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(tconst) REFERENCES films(tconst),
    PRIMARY KEY(user_id, tconst)
);

CREATE TABLE names(
    nconst TEXT NOT NULL PRIMARY KEY,
    primary_name TEXT,
    birth_year INTEGER,
    death_year INTEGER,
    primary_profession TEXT,
    known_for_titles TEXT
);

CREATE TABLE crew(
    tconst TEXT NOT NULL,
    ordering INTEGER,
    nconst TEXT NOT NULL,
    category TEXT,
    job TEXT,
    characters TEXT,
    PRIMARY KEY(tconst, nconst, ordering),
    FOREIGN KEY(tconst) REFERENCES films(tconst),
    FOREIGN KEY(nconst) REFERENCES names(nconst)
);
