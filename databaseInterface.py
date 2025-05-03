import sqlite3 as sl


def createTable():
    con = sl.connect('messages.db')
    cursor = con.cursor()
    with con:
        cursor.execute("CREATE TABLE IF NOT EXISTS messages(user_id BIGINT NOT NULL, chat_id BIGINT NOT NULL, "
                       "text TEXT NOT NULL, sending_time TIMESTAMP NOT NULL, is_sent INT default 0)")
    con.commit()
    con.close()


def getUnsentMessage():
    con = sl.connect('messages.db')
    cursor = con.cursor()
    with con:
        cursor.execute("SELECT * from messages WHERE is_sent = 0")
        messages = cursor.fetchall()
    con.commit()
    con.close()
    return messages


def clear():
    con = sl.connect('messages.db')
    cursor = con.cursor()
    with con:
        cursor.execute("DELETE FROM messages WHERE is_sent = 1")
    con.commit()
    con.close()
