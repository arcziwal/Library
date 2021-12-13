from flask import Flask, request, render_template
from models import Author, Book
from psycopg2 import connect, OperationalError
import os

DATABASE_URL = os.environ['DATABASE_URL']

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello and welcome on my site"


@app.route('/add_book', methods=['GET', 'POST'])
def add_book_to_db():
    cnx = connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
    cursor = cnx.cursor()
    cnx.autocommit = True
    if request.method == "GET":
        authors = Author.load_all_authors(cursor)
        cursor.close()
        cnx.close()
        authors_data = []
        for author in authors:
            authors_data.append(f"{author.full_name}")
        return render_template("add_book_form.html", authors=authors_data)
    elif request.method == "POST":
        book_title = request.form["book_title"]
        book_isbn = request.form["isbn"]
        book_author = request.form["author"]
        book_description = request.form["description"]
        author_id = Author.load_author_by_full_name(cursor, book_author)
        book = Book(book_title, book_isbn, author_id, book_description)
        book.save_to_db(cursor)
        cursor.close()
        cnx.close()
        return f"Książka pod tytułem {book_title} została pomyślnie dodana do bazy danych"


@app.route('/books', methods=['GET'])
def show_all_books():
    cnx = connect(DATABASE_URL, sslmode='require')
    cursor = cnx.cursor()
    cnx.autocommit = True
    books = Book.load_all_books(cursor)
    data_to_show = []
    for book in books:
        author_name = Author.load_author_by_id(cursor, book.author_id)
        data_to_show.append((book.title, author_name, book.isbn))
    cursor.close()
    cnx.close()
    return render_template("book_list.html", books=data_to_show)


@app.route("/book_details/<int:book_index>", methods=['GET'])
def show_book_details(book_index):
    cnx = connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
    cursor = cnx.cursor()
    cnx.autocommit = True
    book = Book.load_book_by_id(cursor, book_index)
    return f"""
<h3>Tytuł:</h3> <p>{book.title}</p>
<h3>Autor:</h3> <p>{Author.load_author_by_id(cursor, book.author_id)}</p>
<h3>Numer ISBN:</h3> <p>{book.isbn}</p>
<h3>Opis:</h3> <p>{book.description}</p>
    """



