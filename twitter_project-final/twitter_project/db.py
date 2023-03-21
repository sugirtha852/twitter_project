import sqlite3

conn = sqlite3.connect("database.db")

c = conn.cursor()

c.execute(
    """CREATE TABLE tweet
             (id INTEGER PRIMARY KEY,
              username TEXT,
              text TEXT,
              updated_at DATE,
              created_at DATE,
              retweet_count INTEGER,
              favorite_count INTEGER,
              lang TEXT
              )"""
)

conn.commit()
c.close()
conn.close()
