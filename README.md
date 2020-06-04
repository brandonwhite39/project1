# Project 1

Web Programming with Python and JavaScript

Welcome to my Books Project!

Initially you are brought to the home page where you can register,
or log in if you already have an account.

Upon sign in, you are able to click the button to Search for a Book
After clicking the button you can search for a book via
the title, ISBN or author name

After finding successful matches you can click the isbn link to
view more details about the book

More details include: title, author, publication year, 
goodreads number of ratings, goodreads average score out of 5,
and any reviews left on the webpage.

You can also access the /api/<ibsn> route to view the asked for information
in json format. If the isbn is invalid, a json saying error is returned
with a 404 response.

Hope you enjoy!

File contents:

application.py - contains all the routing of information+storing info
create.sql - contains SQL code for creating databases
import.py - contains python code for inputting all information in books.csv
templates folder - contains all html code for webpages

