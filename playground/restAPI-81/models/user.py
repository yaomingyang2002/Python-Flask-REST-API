import sqlite3

class UserModel:

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod # so use cls->self
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        # the params always a tuple, so need(), add"," in (username,) to make sense
        row = result.fetchone()
        if row:
            # user = User(row[0], row[1], row[2])
            # user = cls(row[0], row[1], row[2])  # cls= class User
            user = cls(*row) # for multiple row *=3
        else:
            user = None

        connection.close()
        return user

    @classmethod # so use cls->self
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row) # for multiple row *=3
        else:
            user = None

        connection.close()
        return user