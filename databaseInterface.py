import sqlite3 as sl

con = sl.connect('messages.db')


def createTable():
    with con:
        con.execute("CREATE TABLE IF NOT EXISTS messages(user_id BIGINT NOT NULL,"
                    "chat_id BIGINT NOT NULL,"
                    "text TEXT NOT NULL,"
                    "send_at TIMESTAMP NOT NULL,"
                    "is_sent BOOLEAN DEFAULT FALSE)")
