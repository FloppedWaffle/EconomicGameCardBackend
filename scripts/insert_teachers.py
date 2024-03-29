import sqlite3
import openpyxl
import random
import string
import os
from hashlib import sha256
from db_manager import SQLITE_PATH

with sqlite3.connect(SQLITE_PATH) as con:
    cur = con.cursor()

    cur.execute("""DROP TABLE IF EXISTS teachers;""")

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
    
    TEACHERS_XLSX = os.path.join("data", "teachers.xlsx")
    xls = openpyxl.open(TEACHERS_XLSX)
    sheet = xls.active

    for row in range(2, sheet.max_row + 1):
        firstname = sheet['A' + str(row)].value.strip()
        middlename = sheet['B' + str(row)].value.strip()
        subject_name = sheet['C' + str(row)].value.strip()
        uid = sheet['D' + str(row)].value.strip()

        if len(sheet['E' + str(row)].value) < 10:
            characters = (string.ascii_letters + string.digits).replace('I', '', 1).replace('l', '', 1)
            password = ''.join(random.choice(characters) for _ in range(10))
        else:
            password = sheet['E' + str(row)].value.strip()

        password_hash = sha256(password.encode("UTF-8")).hexdigest()


        cur.execute("""
                    INSERT INTO teachers(nfc_uid, password, firstname, middlename, subject_name, balance)
                    VALUES(?, ?, ?, ?, ?, 0)
                    """, (uid, password_hash, firstname, middlename, subject_name, ))
        
        sheet['E' + str(row)] = password
        
    xls.save(TEACHERS_XLSX)
    xls.close()