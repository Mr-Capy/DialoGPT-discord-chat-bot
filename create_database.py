import sqlite3
import os

folder = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(folder, "data.db")

data = sqlite3.connect(db_path)
cur = data.cursor()

cur.execute("CREATE TABLE channels(guild INTEGER NOT NULL, channel INTEGER NOT NULL, PRIMARY KEY (guild, channel))")
cur.execute("CREATE TABLE mod_roles(guild INTEGER NOT NULL, role INTEGER NOT NULL,  PRIMARY KEY (guild, role))")
data.commit()