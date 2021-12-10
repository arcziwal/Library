from flask import Flask, request, render_template
from models import Author
from psycopg2 import connect, OperationalError

USER = "postgres"
PASSWORD = "coderslab"
HOST = "localhost"
DATABASE = "library_db"

app = Flask(__name__)


@app.route('/add_book', methods=['GET', 'POST'])
def main():
    if request.method == "GET":
        cnx = connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
        cursor = cnx.cursor()
        authors = Author.load_all_authors(cursor)
        cursor.close()
        cnx.close()
        authors_data = []
        for author in authors:
            authors_data.append(f"{author.last_name} {author.first_name}")
        return render_template("add_book_form.html", authors=authors_data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


