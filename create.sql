CREATE TABLE books(
    isbn VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE review(
    isbn INTEGER PRIMARY KEY,
    rating FLOAT,
    comments VARCHAR
);
