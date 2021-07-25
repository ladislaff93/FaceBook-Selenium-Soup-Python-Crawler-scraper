import sqlite3


def create_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE UBYTOVANIE
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    TEXT INZERATU TEXT,
                    LINK TEXT);
                ''')


def insert_db(text, link):
    conn = sqlite3.connect('database.db')
    conn.execute(f'''INSERT INTO UBYTOVANIE
                     (TEXT INZERATU, LINK)\
                     VALUES({text},{link});''')
    conn.commit()
    conn.close()
