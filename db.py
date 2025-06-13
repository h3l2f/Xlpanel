import sqlite3
import json

with open("config.json","r", encoding="utf-8") as f:
    config = json.load(f)

def connect():
    conn = sqlite3.connect(config["database"])
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user
                (
                    user varchar(255) PRIMARY KEY,
                    password varchar(255), 
                    email varchar(255),
                    slot bigint(255),
                    cpu bigint(255),
                    disk bigint(255),
                    ram bigint(255),
                    coin bigint(255),
                    verified int(1) default 0,
                    lastSend int(255) default 0,
                    banned int(255) default 0
                )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS session
                (
                    sid varchar(255) PRIMARY KEY,
                    passport varchar(255),
                    alive varchar(255)
                )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS verify
                (
                    user varchar(255) PRIMARY KEY,
                    email varchar(255),
                    code varchar(255)
                )''')
    conn.commit()
    return conn

# connect()