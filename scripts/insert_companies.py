import sqlite3
import openpyxl
import random
import string
import os
from hashlib import sha256
from db_manager import SQLITE_PATH

with sqlite3.connect(SQLITE_PATH) as con:
    cur = con.cursor()

    cur.execute("""DROP TABLE IF EXISTS companies;""")

    cur.execute("""
                CREATE TABLE IF NOT EXISTS companies(
                company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                password VARCHAR(64) NOT NULL UNIQUE,
                name VARCHAR(256) NOT NULL UNIQUE,
                balance INTEGER NOT NULL,
                profit INTEGER NOT NULL,
                tax_percentage FLOAT NOT NULL,
                taxes INTEGER NOT NULL,
                is_state INTEGER NOT NULL)
                """)
    
    COMPANIES_XLSX = os.path.join("data", "companies.xlsx")
    xls = openpyxl.open(COMPANIES_XLSX)
    sheet = xls.active

    for row in range(2, sheet.max_row + 1):
        company_id = sheet['A' + str(row)].value
        name = sheet['B' + str(row)].value.strip()
        is_state = sheet['C' + str(row)].value
        tax_percentage = sheet['D' + str(row)].value
        
        if not sheet['E' + str(row)].value:
            characters = (string.ascii_letters + string.digits).replace('I', '', 1).replace('l', '', 1)
            password = ''.join(random.choice(characters) for _ in range(10))
        else:
            password = sheet['E' + str(row)].value
        
        password_hash = sha256(password.encode("UTF-8")).hexdigest()


        cur.execute("""
                    INSERT INTO companies(company_id, password, name, balance, profit, tax_percentage, taxes, is_state)
                    VALUES(?, ?, ?, 0, 0, ?, 0, ?)
                    """, (company_id, password_hash, name, tax_percentage, is_state, ))
        
        sheet['E' + str(row)] = password

    xls.save(COMPANIES_XLSX)
    xls.close()