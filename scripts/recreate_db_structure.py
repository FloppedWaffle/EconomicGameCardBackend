import sqlite3
from db_manager import SQLITE_PATH


with sqlite3.connect(SQLITE_PATH) as con:
    cur = con.cursor()

    cur.execute("""DROP TABLE IF EXISTS players;""")
    cur.execute("""DROP TABLE IF EXISTS teachers;""")
    cur.execute("""DROP TABLE IF EXISTS companies;""")
    cur.execute("""DROP TABLE IF EXISTS services;""")
    cur.execute("""DROP TABLE IF EXISTS bankers;""")
    cur.execute("""DROP TABLE IF EXISTS atm;""")


    cur.execute("""
                CREATE TABLE IF NOT EXISTS players(
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                nfc_uid VARCHAR(32) NOT NULL UNIQUE,
                firstname VARCHAR(32) NOT NULL,
                lastname VARCHAR(32) NOT NULL,
                grade VARCHAR(16) NOT NULL,
                balance INTEGER NOT NULL,
                tax_paid INTEGER NOT NULL,
                company_id INTEGER NOT NULL,
                is_founder INTEGER NOT NULL,
                is_minister INTEGER NOT NULL,
                is_minister_paid INTEGER)
                """)
    

    cur.execute("""
                CREATE TABLE IF NOT EXISTS teachers(
                teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                nfc_uid VARCHAR(32) NOT NULL UNIQUE,
                password VARCHAR(64) NOT NULL UNIQUE,
                firstname VARCHAR(32) NOT NULL,
                middlename VARCHAR(32) NOT NULL,
                subject_name VARCHAR(256) NOT NULL UNIQUE,
                balance INTEGER NOT NULL)
                """)
    

    cur.execute("""
                CREATE TABLE IF NOT EXISTS companies(
                company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                password VARCHAR(64) NOT NULL UNIQUE,
                name VARCHAR(256) NOT NULL UNIQUE,
                balance INTEGER NOT NULL,
                profit INTEGER NOT NULL,
                taxes INTEGER NOT NULL,
                is_state INTEGER NOT NULL)
                """)
    

    cur.execute("""
                CREATE TABLE IF NOT EXISTS services(
                service_id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                name VARCHAR(64) NOT NULL UNIQUE,
                quantity INTEGER NOT NULL,
                cost INTEGER NOT NULL)
                """)
    


    cur.execute("""
                CREATE TABLE IF NOT EXISTS bankers(
                banker_id INTEGER PRIMARY KEY AUTOINCREMENT,
                password VARCHAR(64) NOT NULL UNIQUE)
                """)
    

    cur.execute("""
                CREATE TABLE IF NOT EXISTS atm(
                atm_id INTEGER PRIMARY KEY AUTOINCREMENT,
                password VARCHAR(64) NOT NULL UNIQUE)
                """)
    

    con.commit()