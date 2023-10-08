from flask import Blueprint, request, jsonify
import sqlite3
from .func_utils import check_authorization, logger, SQLITE_PATH


bankers_bp = Blueprint("bankers", __name__)

@bankers_bp.route("/banker", methods=["GET"])
@check_authorization
def get_banker(sub=None, role=None):
    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT banker_id
                    FROM bankers
                    WHERE password = ?;
                    """, (sub, ))
        banker = cur.fetchone()
        if not banker:
            return "404", 404
        

    return "200"



@bankers_bp.route("/banker/get_person", methods=["POST"])
@check_authorization
def get_person(sub=None, role=None):
    uid = request.get_json().get("uid")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        role = "players"
        cur.execute("""
                    SELECT firstname, lastname, grade, balance, tax_paid, is_founder, is_minister, is_minister_paid
                    FROM players
                    WHERE nfc_uid = ?;
                    """, (uid, ))
        person = cur.fetchone()
        if not person:
            role = "teachers"
            cur.execute("""
                        SELECT firstname, middlename, balance
                        FROM teachers
                        WHERE nfc_uid = ?;
                        """, (uid, ))
            person = cur.fetchone()
        if not person:
            return "404", 404


    return jsonify(role=role, person=person)



@bankers_bp.route("/banker/transfer_money", methods=["POST"])
@check_authorization
def transfer_money(sub=None, role=None):
    uid = request.get_json().get("uid")
    amount = request.get_json().get("amount")
    transfer_action = request.get_json().get("transfer_action")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        person_table = "players"
        cur.execute("""
                    SELECT balance
                    FROM players
                    WHERE nfc_uid = ?;
                    """, (uid, ))
        person = cur.fetchone()
        if not person:
            person_table = "teachers"
            cur.execute("""
                        SELECT balance
                        FROM teachers
                        WHERE nfc_uid = ?;
                        """, (uid, ))
            person = cur.fetchone()
            if not person:
                 return "404", 404


        cur.execute(f"""
                    SELECT balance
                    FROM {person_table}
                    WHERE nfc_uid = ?;
                    """, (uid, ))
        balance = cur.fetchone()[0]
        if (amount > balance and transfer_action == "withdraw"):
            return "400", 400
        

        if (transfer_action == "deposit"):
            cur.execute(f"""
                        UPDATE {person_table}
                        SET balance = balance + ?
                        WHERE nfc_uid = ?;
                        """, (amount, uid, ))
        elif (transfer_action == "withdraw"):
                        cur.execute(f"""
                        UPDATE {person_table}
                        SET balance = balance - ?
                        WHERE nfc_uid = ?;
                        """, (amount, uid, ))
        
        con.commit()
    
    return "200"



@bankers_bp.route("/banker/get_transfer_player", methods=["POST"])
@check_authorization
def get_transfer_player(sub=None, role=None):
    firstname = request.get_json().get("firstname")
    lastname = request.get_json().get("lastname")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT firstname, lastname, grade, player_id
                    FROM players
                    WHERE firstname LIKE ? AND lastname LIKE ?;
                    """, (firstname + '%', lastname + '%', ))
        players = cur.fetchall()

    return jsonify(players=players)



@bankers_bp.route("/banker/transfer_player_money", methods=["POST"])
@check_authorization
def transfer_player_money(sub=None, role=None):
    uid = request.get_json().get("uid")
    player_id = request.get_json().get("player_id")
    amount = request.get_json().get("amount")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        if amount < 1:
            return "400", 400
        
        cur.execute("""
                    SELECT balance
                    FROM players
                    WHERE nfc_uid = ?;
                    """, (uid, ))
        balance = cur.fetchone()[0]
        if amount > balance:
            return "400", 400
        
        cur.execute("""
                    UPDATE players
                    SET balance = balance - ?
                    WHERE nfc_uid = ?;
                    """, (amount, uid, ))
        
        cur.execute("""
                    UPDATE players
                    SET balance = balance + ?
                    WHERE player_id = ?;
                    """, (amount, player_id, ))
        
        con.commit()

    return "200"



@bankers_bp.route("/banker/pay_player_taxes", methods=["POST"])
@check_authorization
def pay_player_taxes(sub=None, role=None):
    uid = request.get_json().get("uid")
    is_card = bool(request.get_json().get("is_card"))

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT tax_paid
                    FROM players
                    WHERE nfc_uid = ?;
                    """, (uid, ))
        tax_paid = cur.fetchone()[0]
        if tax_paid:
            return "400", 400

        cur.execute("""
                    UPDATE players
                    SET tax_paid = 1
                    WHERE nfc_uid = ?;
                    """, (uid, ))
        
        if is_card:
            cur.execute("""
                        UPDATE players
                        SET balance = balance - ?
                        WHERE nfc_uid = ?;
                        """, (10, uid, )) # TODO: ВРЕМЕННЫЙ НАЛОГ, ПОТОМ В КОНФИГ ДОБАВИТЬ НУЖНО НОРМАЛЬНО
        
        con.commit()

    return "200"



@bankers_bp.route("/banker/pay_company_taxes", methods=["POST"])
@check_authorization
def pay_company_taxes(sub=None, role=None):
    uid = request.get_json().get("uid")
    tax_amount = request.get_json().get("tax_amount")
    is_card = bool(request.get_json().get("is_card"))

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT company_id, balance
                    FROM players
                    WHERE nfc_uid = ? AND is_founder = 1;
                    """, (uid, ))
        player = cur.fetchone()
        if not player:
            return jsonify(error="founder_not_found"), 404
        company_id = player[0]
        if is_card:
            balance = player[1]
            if balance < tax_amount:
                return "400", 400
    
        cur.execute("""
                    SELECT taxes
                    FROM companies
                    WHERE company_id = ?;
                    """, (company_id, ))
        company = cur.fetchone()
        if not company:
            return jsonify(error="company_not_found"), 404
        taxes = company[0]
        if tax_amount > taxes:
            tax_amount = taxes

        cur.execute("""
                    UPDATE companies
                    SET taxes = taxes - ?
                    WHERE company_id = ?;
                    """, (tax_amount, company_id, ))
        if is_card:
            cur.execute("""
                        UPDATE players
                        SET balance = balance - ?
                        WHERE nfc_uid = ?;
                        """, (tax_amount, uid, ))
            
        con.commit()

    return "200"



@bankers_bp.route("/banker/pay_minister_salary", methods=["POST"])
@check_authorization
def pay_minister_salary(sub=None, role=None):
    uid = request.get_json().get("uid")
    is_card = bool(request.get_json().get("is_card"))

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT is_minister_paid
                    FROM players
                    WHERE nfc_uid = ? AND is_minister = 1;
                    """, (uid, ))
        minister = cur.fetchone()
        if not minister:
            return "404", 404
        is_minister_paid = minister[0]

        if is_minister_paid:
            return "400", 400
        
        if is_card:
            cur.execute("""
                        UPDATE players
                        SET balance = balance + ?
                        WHERE nfc_uid = ?;
                        """, (125, uid, )) # TODO: ВРЕМЕННАЯ ЗАРПЛАТА, ПОТОМ В КОНФИГ ДОБАВИТЬ НУЖНО НОРМАЛЬНО

        cur.execute("""
                    UPDATE players
                    SET is_minister_paid = 1
                    WHERE nfc_uid = ?;
                    """, (uid, ))
        
        con.commit()

    return "200"