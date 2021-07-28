import sqlite3


def create_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE UBYTOVANIE
                    (INZERAT TEXT,
                     LINK TEXT);
                ''')


def insert_db(text, link):
    info = [text, link]
    conn = sqlite3.connect('database.db')
    conn.execute('''INSERT INTO UBYTOVANIE
                    VALUES(?,?)''', info)
    conn.commit()
    conn.close()
