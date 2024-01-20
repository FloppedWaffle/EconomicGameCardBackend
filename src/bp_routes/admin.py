from flask import Blueprint, request, jsonify, render_template
import sqlite3
from .func_utils import logger, SQLITE_PATH

admin_bp = Blueprint("admin", __name__)



@admin_bp.route("/admin/register_person", methods=["POST"])
def register_person():
    firstname = request.get_json().get("firstname")
    lastname = request.get_json().get("lastname")
    grade = request.get_json().get("grade")
    is_minister = int(bool(request.get_json().get("is_minister")))
    uid = request.get_json().get("uid")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT *
                    FROM players
                    WHERE (firstname LIKE ? AND lastname LIKE ?) OR nfc_uid = ?;
                    """, (firstname, lastname, uid, ))
        person = cur.fetchone()
        if person:
            return "400", 400
    
        cur.execute("""
                INSERT INTO players(firstname, lastname, grade, balance, tax_paid, is_minister, is_minister_paid, nfc_uid, is_founder, company_id)
                VALUES(?, ?, ?, 0, 0, ?, 0, ?, 0, 0);
                """, (firstname, lastname, grade, is_minister, uid, ))

        con.commit()
    
    return "200"



@admin_bp.route("/admin/register_company", methods=["POST"])
def register_company():
    company_name = request.get_json().get("company_name")
    password = request.get_json().get("password")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT *
                    FROM companies
                    WHERE name LIKE ? OR password = ?;
                    """, (company_name, password))
        company = cur.fetchone()
        if company:
            return "400", 400
    
        cur.execute("""
                    INSERT INTO companies(password, name, balance, taxes, profit, is_state) 
                    VALUES(?, ?, 0, 0, 0, 0);
                    """, (password, company_name, ))

        con.commit()
    
    return "200"