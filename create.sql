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
    id SERIAL REFERENCES users(id),
    PRIMARY KEY (id)
);


CREATE TABLE users(
    id SERIAL UNIQUE,
    username VARCHAR,
    password VARCHAR,
    PRIMARY KEY (id)
);