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
                    WHERE (firstname LIKE ? AND lastname LIKE ?) OR (lastname LIKE ? AND firstname LIKE ?) OR nfc_uid = ?;
                    """, (firstname, lastname, firstname, lastname, uid, ))
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



@admin_bp.route("/admin/register_teacher", methods=["POST"])
def register_teacher():
    firstname = request.get_json().get("firstname")
    middlename = request.get_json().get("middlename")
    subject_name = request.get_json().get("subject_name")
    uid = request.get_json().get("uid")
    password = request.get_json().get("password")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT *
                    FROM teachers
                    WHERE (firstname LIKE ? AND middlename LIKE ?) OR (middlename LIKE ? AND firstname LIKE ?) OR nfc_uid = ? OR password = ?;
                    """, (firstname, middlename, firstname, middlename, uid, password))
        person = cur.fetchone()
        if person:
            return "400", 400
    
        cur.execute("""
                INSERT INTO teachers(firstname, middlename, subject_name, nfc_uid, password, balance)
                VALUES(?, ?, ?, ?, ?, 0);
                """, (firstname, middlename, subject_name, uid, password))

        con.commit()
    
    return "200"



@admin_bp.route("/admin/get_persons", methods=["POST"])
def get_students(sub=None, role=None):
    firstname = request.get_json().get("firstname")
    lastname = request.get_json().get("lastname")
    

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT firstname, lastname, grade, player_id 
                    FROM players 
                    WHERE firstname LIKE ? AND lastname LIKE ?;
                    """, (firstname + "%", lastname + "%", ))
        players = cur.fetchall()
        

    return jsonify(players=players)



@admin_bp.route("/admin/get_person_balance", methods=["POST"])
def get_person_balance():
    player_id = request.get_json().get("player_id")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT balance
                    FROM players
                    WHERE player_id = ?;
                    """, (player_id, ))
        balance = cur.fetchone()[0]


    return jsonify(balance=balance)



@admin_bp.route("/admin/get_companies", methods=["POST"])
def get_companies():
    company_name = request.get_json().get("company_name");

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT name, company_id
                    FROM companies
                    WHERE name LIKE ?;
                    """, (company_name + "%", ))
        companies = cur.fetchall()

    return jsonify(companies=companies)



@admin_bp.route("/admin/get_company_info", methods=["POST"])
def get_company_info():
    company_id = request.get_json().get("company_id");

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT balance
                    FROM companies
                    WHERE company_id = ?;
                    """, (company_id, ))
        balance = cur.fetchone()[0]

        cur.execute("""
                    SELECT service_id, name, cost, quantity
                    FROM services 
                    WHERE company_id = ?;
                    """, (company_id, ))
        services = cur.fetchall()

    return jsonify(balance=balance, services=services)



@admin_bp.route("/admin/add_person_to_company", methods=["POST"])
def add_person_to_company():
    player_id = request.get_json().get("player_id")
    company_id = request.get_json().get("company_id")
    is_founder = bool(request.get_json().get("is_founder"))

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT player_id
                    FROM players
                    WHERE player_id = ? AND company_id = 0 AND is_minister = 0;
                    """, (player_id, ))
        person = cur.fetchone()
        if not person:
            return "400", 400
        

        cur.execute("""
                    UPDATE players
                    SET company_id = ?, is_founder = ?
                    WHERE player_id = ?;
                    """, (company_id, is_founder, player_id, ))
        
        if (is_founder):
                    cur.execute("""
                        UPDATE players
                        SET tax_paid = 1
                        WHERE player_id = ?;
                        """, (player_id, ))
        
        con.commit()

    return "200"



@admin_bp.route("/admin/remove_person_from_company", methods=["POST"])
def remove_person_from_company():
    player_id = request.get_json().get("player_id")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT player_id
                    FROM players
                    WHERE player_id = ? AND company_id != 0;
                    """, (player_id, ))
        person = cur.fetchone()
        if not person:
            return "400", 400
        

        cur.execute("""
                    UPDATE players
                    SET company_id = 0, is_founder = 0
                    WHERE player_id = ?;
                    """, (player_id, ))
        
        con.commit()

    return "200"



@admin_bp.route("/admin/remove_person", methods=["POST"])
def remove_person():
    player_id = request.get_json().get("player_id")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    DELETE 
                    FROM players
                    WHERE player_id = ?;
                    """, (player_id, ))
        
        con.commit()

    return "200"



@admin_bp.route("/admin/remove_company", methods=["POST"])
def remove_company():
    company_id = request.get_json().get("company_id")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    DELETE 
                    FROM companies
                    WHERE company_id = ?;
                    """, (company_id, ))
        
        cur.execute("""
                    DELETE
                    FROM services
                    WHERE company_id = ?;
                    """, (company_id, ))
        
        con.commit()

    return "200"



@admin_bp.route("/admin/add_company_service", methods=["POST"])
def add_company_service():
    company_id = request.get_json().get("company_id")
    service_name = request.get_json().get("service_name")
    service_cost = request.get_json().get("service_cost")
    service_quantity = request.get_json().get("service_quantity")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT name
                    FROM services
                    WHERE company_id = ? AND name LIKE ?;
                    """, (company_id, service_name + "%"))
        service = cur.fetchone()
        if service:
            return "400", 400
        
        cur.execute("""
                    INSERT INTO services(company_id, name, quantity, cost)
                    VALUES (?, ?, ?, ?);
                    """, (company_id, service_name, service_quantity, service_cost, ))
        
        con.commit()

    return "200"



@admin_bp.route("/admin/remove_company_service", methods=["POST"])
def remove_company_service():
    company_id = request.get_json().get("company_id")
    services = request.get_json().get("services")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        for service_id in services:
            cur.execute("""
                        DELETE
                        FROM services
                        WHERE service_id = ?;
                        """, (service_id, ))
        
        con.commit()

    return "200"