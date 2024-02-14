import sqlite3
import openpyxl
import os
from db_manager import SQLITE_PATH

with sqlite3.connect(SQLITE_PATH) as con:
    cur = con.cursor()

    cur.execute("""DROP TABLE IF EXISTS services;""")

    cur.execute("""
                CREATE TABLE IF NOT EXISTS services(
                service_id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                name VARCHAR(64) NOT NULL,
                quantity INTEGER NOT NULL,
                cost INTEGER NOT NULL)
                """)
    
    SERVICES_XLSX = os.path.join("data", "services.xlsx")
    xls = openpyxl.open(SERVICES_XLSX)
    sheet = xls.active

    for row in range(2, sheet.max_row + 1):
        company_id = sheet['A' + str(row)].value
        name = sheet['B' + str(row)].value.strip()
        quantity = sheet['C' + str(row)].value
        cost = sheet['D' + str(row)].value


        cur.execute("""
                    INSERT INTO services(company_id, name, quantity, cost)
                    VALUES(?, ?, ?, ?)
                    """, (company_id, name, quantity, cost, ))

    xls.save(SERVICES_XLSX)
    xls.close()