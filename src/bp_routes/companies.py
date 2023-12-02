from flask import Blueprint, request, jsonify
import sqlite3
from .func_utils import check_authorization, logger, SQLITE_PATH


TAX = 0.1

companies_bp = Blueprint("companies", __name__)


@companies_bp.route("/company", methods=["GET"])
@check_authorization
def get_company(sub=None, role=None):
    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                        SELECT name, balance, profit, taxes, is_state, company_id FROM companies WHERE password = ?;
                    """, (sub, ))
        company = cur.fetchone()
        if not company:
            return "404", 404
        name = company[0]
        balance = str(company[1])
        profit = str(company[2])
        taxes = str(company[3])
        is_state = bool(company[4])
        company_id = company[5]
    
        cur.execute("""
                    SELECT firstname, lastname FROM players WHERE company_id = ? AND is_founder = 1
                    """, (company_id, ))
        founders = cur.fetchall()
        if not founders and not is_state:
            return "404", 404
        
        cur.execute("""
                    SELECT service_id, name, cost, quantity
                    FROM services 
                    WHERE company_id = ? AND quantity > 0;
                    """, (company_id, ))
        services = cur.fetchall()

    return jsonify(name=name, balance=balance, profit=profit, 
                   tax_paid=taxes, is_state=is_state, founders=founders, 
                   services=services)



@companies_bp.route("/company/get_founders", methods=["POST"])
@check_authorization
def get_founder(sub=None, role=None):
    firstname = request.get_json().get("firstname")
    lastname = request.get_json().get("lastname")
    
    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT company_id FROM companies 
                    WHERE password = ?;
                    """, (sub, ))
        company_id = cur.fetchone()[0]

        cur.execute("""
                    SELECT firstname, lastname, player_id FROM players 
                    WHERE firstname LIKE ? AND lastname LIKE ? AND is_minister = 0 AND company_id = ? AND is_founder = 1;
                    """, (firstname + "%", lastname + "%", company_id, ))
        founders = cur.fetchall()
        
    return jsonify(founders=founders)
    


@companies_bp.route("/company/pay_founder", methods=["POST"])
@check_authorization
def pay_founder(sub=None, role=None):
    player_id = request.get_json().get("player_id")
    withdraw = request.get_json().get("withdraw")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT company_id 
                    FROM players 
                    WHERE player_id = ?;
                    """, (player_id, ))
        company_id = cur.fetchone()
        if not company_id:
            return "404", 404
        company_id = company_id[0]

        cur.execute("""
                    SELECT balance FROM companies 
                    WHERE company_id = ?;
                    """, (company_id, ))
        balance = cur.fetchone()[0]
        if balance < withdraw or withdraw < 1:
            return "400", 400

        cur.execute("""
                    UPDATE companies 
                    SET balance = balance - ? 
                    WHERE company_id = ?
                    """, (withdraw, company_id, ))
        cur.execute("""
                    UPDATE players 
                    SET balance = balance + ? 
                    WHERE player_id = ?
                    """, (withdraw, player_id, ))
        
        con.commit()
        
    return "200"



@companies_bp.route("/company/pay_services", methods=["POST"])
@check_authorization
def pay_services(sub=None, role=None):
    uid = request.get_json().get("uid")
    services = request.get_json().get("services")

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        if uid:
            person_table = "players"
            cur.execute("""
                        SELECT player_id, balance
                        FROM players
                        WHERE nfc_uid = ?;
                        """, (uid, ))
            person = cur.fetchone()
            if not person:
                person_table = "teachers"
                cur.execute("""
                            SELECT teacher_id, balance
                            FROM teachers
                            WHERE nfc_uid = ?;
                            """, (uid, ))
                person = cur.fetchone()
            if not person:
                return "404", 404
            balance = person[1]
            

        cur.execute("""
                    SELECT company_id
                    FROM companies
                    WHERE password = ?;
                    """, (sub, ))
        company_id = cur.fetchone()[0]
        

        all_cost = 0
        for pair in services:
            service_id = pair["service_id"]
            quantity = pair["quantity"]
            cur.execute("""
                        SELECT cost
                        FROM services
                        WHERE service_id = ? AND quantity >= ?;
                        """, (service_id, quantity, ))
            cost = cur.fetchone()
            if not cost:
                return jsonify(error="no_enough_quantity"), 400
            
            all_cost += cost[0] * quantity
            

        if uid:
            if balance < all_cost:
                return jsonify(error="not_enough_money"), 400
                
            cur.execute(f"""
                        UPDATE {person_table}
                        SET balance = balance - ?
                        WHERE nfc_uid = ?;
                        """, (all_cost, uid, ))
        
            cur.execute("""
                        UPDATE companies
                        SET balance = balance + ?, profit = profit + ?
                        WHERE company_id = ?;
                        """, (all_cost, all_cost, company_id, ))
        else:
            cur.execute("""
                        UPDATE companies
                        SET profit = profit + ?
                        WHERE company_id = ?;
                        """, (all_cost, company_id, ))
            

        for pair in services:
            service_id = pair["service_id"]
            quantity = pair["quantity"]
            cur.execute("""
                        UPDATE services
                        SET quantity = quantity - ?
                        WHERE service_id = ?;
                        """, (quantity, service_id, ))
        
        con.commit()


    return "200"