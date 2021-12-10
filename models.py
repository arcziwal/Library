class Author:
    def __init__(self, first_name="", last_name=""):
        self._id = -1
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = f"{self.last_name} {self.first_name}"

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:

            sql = "INSERT INTO authors(first_name, last_name, full_name) VALUES (%s, %s, %s) RETURNING id"
            values = (self.first_name, self.last_name, self.full_name)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = "UPDATE authors SET first_name=%s, last_name=%s, full_name=%s WHERE id=%s"
            values = (self.first_name, self.last_name, self.full_name, self._id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_authors(cursor):
        sql = "SELECT id, first_name, last_name, full_name FROM authors"
        authors = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, first_name, last_name, full_name = row
            author = Author()
            author._id = id_
            author.first_name = first_name
            author.last_name = last_name
            author.full_name = full_name
            authors.append(author)
        return authors

    @staticmethod
    def load_author_by_full_name(cursor, author_full_name):
        sql = f"SELECT id FROM authors WHERE full_name=%s"
        value = str(author_full_name)
        print(value)
        cursor.execute(sql, (value,))
        author_id = cursor.fetchone()[0]
        return author_id

    @staticmethod
    def load_author_by_id(cursor, author_id):
        sql = f"SELECT full_name FROM authors WHERE id=%s"
        cursor.execute(sql, (author_id,))
        author_full_name = cursor.fetchone()[0]
        return author_full_name

class Book:
    def __init__(self, title="", isbn="", author_id=-1, description=""):
        self._id = -1
        self.title = title
        self.isbn = isbn
        self.author_id = author_id
        self.description = description

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = "INSERT INTO books(title, isbn, author_id, description) VALUES (%s, %s, %s, %s) RETURNING id"
            values = (self.title, self.isbn, self.author_id, self.description)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = "UPDATE books SET title=%s, isbn=%s, author_id=%s, description=%s WHERE id=%s"
            values = (self.title, self.isbn, self.author_id, self.description, self._id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_books(cursor):
        sql = "SELECT id, title, isbn, author_id, description FROM books"
        books = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, title, isbn, author_id, description = row
            book = Book()
            book._id = id_
            book.title = title
            book.isbn = isbn
            book.author_id = author_id
            book.description = description
            books.append(book)
        return books

