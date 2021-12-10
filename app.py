from flask import Flask
from models import Author
from psycopg2 import connect, OperationalError

USER = "postgres"
PASSWORD = "coderslab"
HOST = "localhost"
DATABASE = "library_db"

app = Flask(__name__)


@app.route('/add_to_db')
def main():
    cnx = connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cnx.autocommit = True
    cursor = cnx.cursor()
    author = Author("Artur", "Waligóra")
    author.save_to_db(cursor)
    cursor.close()
    cnx.close()
    return f"Dodano do bazy danych autorów pozycję {author.id}: {author.first_name} {author.last_name}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


