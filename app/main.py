from flask import Flask, request, render_template
from models import Author, Book
from psycopg2 import connect
import verifier
import os

DATABASE_URL = os.environ['DATABASE_URL']
LOCAL_HOST = "127.0.0.1"
LOCAL_DB = "library_db"
LOCAL_USER = "postgres"
LOCAL_PASSWORD = "coderslab"

app = Flask(__name__)


def connect_to_test_db():
    cnx = connect(user=LOCAL_USER, password=LOCAL_PASSWORD, host=LOCAL_HOST, database=LOCAL_DB)
    cnx.autocommit = True
    cursor = cnx.cursor()
    return cnx, cursor


def connect_to_production_db():
    cnx = connect(DATABASE_URL, sslmode='require')
    cnx.autocommit = True
    cursor = cnx.cursor()
    return cnx, cursor


@app.route('/')
def index():
    return "Hello and welcome on my site"


@app.route('/add_book', methods=['GET', 'POST'])
def add_book_to_db():
    cnx, cursor = connect_to_production_db()
    if request.method == "GET":
        authors = Author.load_all_authors(cursor)
        cursor.close()
        cnx.close()
        authors_data = []
        for author in authors:
            authors_data.append(f"{author.full_name}")
        return render_template("add_book_form.html", authors=authors_data)
    elif request.method == "POST":
        data_to_get = ['book_title', 'isbn', 'author', 'description']
        received_data = []
        for data in data_to_get:
            print(data)
            if verifier.if_not_empty(request.form[str(data)]):
                received_data.append(request.form[str(data)])
            else:
                return render_template("invalid_data_for_new_book.html")
        if not verifier.check_isbn(received_data[1]):
            return render_template("invalid_data_for_new_book.html")
        author_id = Author.load_author_by_full_name(cursor, received_data[2])
        print(f"{received_data}")
        book = Book(received_data[0], received_data[1], author_id, received_data[3])
        if book.check_if_isbn_in_db(cursor):
            book.save_to_db(cursor)
            cursor.close()
            cnx.close()
        else:
            return f"""
<b>Książka o takim numerze ISBN już istnieje w bazie danych</b><br>
<b>Kliknij <a href="/add_book">tutaj</a> aby spróbować ponownie</b>
            """
        return f"Książka pod tytułem {received_data[0]} została pomyślnie dodana do bazy danych"


@app.route('/books', methods=['GET'])
def show_all_books():
    cnx, cursor = connect_to_production_db()
    books = Book.load_all_books(cursor)
    data_to_show = []
    for book in books:
        author_name = Author.load_author_by_id(cursor, book.author_id)
        data_to_show.append((book.title, author_name, book.isbn, book.id))
    cursor.close()
    cnx.close()
    return render_template("book_list.html", books=data_to_show)


@app.route("/book_details/<int:book_index>", methods=['GET'])
def show_book_details(book_index):
    cnx, cursor = connect_to_production_db()
    book = Book.load_book_by_id(cursor, book_index)
    return f"""
<h3>Tytuł:</h3> <p>{book.title}</p>
<h3>Autor:</h3> <p>{Author.load_author_by_id(cursor, book.author_id)}</p>
<h3>Numer ISBN:</h3> <p>{book.isbn}</p>
<h3>Opis:</h3> <p>{book.description}</p>
    """


@app.route('/add_author', methods=['GET', 'POST'])
def add_author_to_db():
    if request.method == "GET":
        return render_template('add_author_from.html')
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        cnx, cursor = connect_to_production_db()
        author = Author(first_name, last_name)
        if Author.load_author_by_full_name(cursor, author.full_name) is not None:
            return f"Podany autor znajduje się już w bazie. Czy na pewno chcesz go dodać?"
        author.save_to_db(cursor)
        cursor.close()
        cnx.close()
        return f"Autor: <b>{author.full_name}</b> został dodany do bazy danych"


@app.route('/delete_book', methods=['GET', 'POST'])
def delete_book_from_db():
    if request.method == "GET":
        cnx, cursor = connect_to_production_db()
        books = Book.load_all_books(cursor)
        data_to_show = []
        for book in books:
            author_name = Author.load_author_by_id(cursor, book.author_id)
            data_to_show.append((book.title, author_name, book.isbn))
        cursor.close()
        cnx.close()
        return render_template("delete_book_table.html", books=data_to_show)
    elif request.method == "POST":
        cnx, cursor = connect_to_production_db()
        isbn_list = Book.load_isbn_list(cursor)
        books_to_delete = []
        for isbn_tuple in isbn_list:
            for isbn in isbn_tuple:
                if request.form.get(isbn) == "on":
                    books_to_delete.append(Book.load_book_by_isbn(cursor, isbn))
        output_string = ""
        for book in books_to_delete:
            book.delete_book_from_db(cursor)
            output_string += f"Książka pod tytułem <b>{book.title}</b> o numerze <b>{book.isbn}</b> została usunięta z bazy danych<br>"
        return output_string
