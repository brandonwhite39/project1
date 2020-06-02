CREATE TABLE books(
    isbn VARCHAR,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL,
    PRIMARY KEY (isbn)
);

CREATE TABLE review(
    isbn VARCHAR REFERENCES books(isbn),
    rating FLOAT,
    comments VARCHAR,
    PRIMARY KEY (isbn)
);
