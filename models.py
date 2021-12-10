class Author:
    def __init__(self, first_name="", last_name=""):
        self._id = -1
        self.first_name = first_name
        self.last_name = last_name

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = "INSERT INTO authors(first_name, last_name) VALUES (%s, %s) RETURNING id"
            values = (self.first_name, self.last_name)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = "UPDATE authors SET first_name=%s, last_name=%s WHERE id=%s"
            values = (self.first_name, self.last_name, self._id)
            cursor.execute(sql, values)
            return True


class Book:
    def __init__(self, author_id, title="", isbn="", description=""):
        self._id = -1
        self.author_id = author_id
        self.title = title
        self.isbn = isbn
        self.description = description

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = "INSERT INTO books(title, isbn, author_id, desription) VALUES (%s, %s, %s, %s) RETURNING id"
            values = (self.title, self.isbn, self.author_id, self.description)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = "UPDATE books SET title=%s, isbn=%s, author_id=%s, description=%s WHERE id=%s"
            values = (self.title, self.isbn, self.author_id, self.description, self._id)
            cursor.execute(sql, values)
            return True
