import sqlite3

CREATE_USERS_QUERY = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL
);
'''

CREATE_NUMBERS_QUERY = '''
CREATE TABLE IF NOT EXISTS numbers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
'''

class Database():

    def __init__(self, database):
        self.database = database
    
    def __connect(self):
        return sqlite3.connect(self.database)

    def __execute(self, query, params=None):
        if not params:
            params = tuple()
        with self.__connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

    def init_database(self):
        self.__execute(CREATE_USERS_QUERY)
        self.__execute(CREATE_NUMBERS_QUERY)

    def insert_user(self, email):
        if not self.get_user_id(email):
            query = "INSERT INTO users (email) VALUES (?)"
            params = (email,)
            self.__execute(query, params)

    def get_users_numbers(self):
        with self.__connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT u.id as id, u.email as email, n.id as number FROM users as u LEFT JOIN numbers as n ON u.id = n.user_id ORDER BY n.id, u.email")
            result = cursor.fetchall()
        return result    

    def get_user_id(self, email):
        with self.__connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()
        if not result:
            return None
        return result[0]

    def insert_number(self, user_id):
        with self.__connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO numbers (user_id) VALUES (?)", (user_id,))

    def get_number(self, email):
        with self.__connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT numbers.id FROM users INNER JOIN numbers ON users.id = numbers.user_id WHERE users.email = ?", (email,))
            result = cursor.fetchone()
        if not result:
            return
        return result[0]




