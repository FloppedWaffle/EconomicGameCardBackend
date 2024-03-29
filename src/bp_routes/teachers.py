from math import ceil
from flask import Blueprint, request, jsonify
import sqlite3
from .func_utils import check_authorization, logger, SQLITE_PATH

teachers_bp = Blueprint("teachers", __name__)



@teachers_bp.route("/teachers", methods=["GET"])
@check_authorization
def get_teacher_info(sub=None, role=None):
    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()
        
        cur.execute("""
                    SELECT firstname, middlename, balance, subject_name 
                    FROM teachers 
                    WHERE password = ?;
                    """, (sub, ))
        teacher = cur.fetchone()
    if not teacher:
        return "404", 404
    
    name = teacher[0] + " " + teacher[1]
    balance = str(teacher[2])
    subject_name = teacher[3]
    

    return jsonify(name=name, balance=balance, subject_name=subject_name)



@teachers_bp.route("/teachers/get_students", methods=["POST"])
@check_authorization
def get_students(sub=None, role=None):
    firstname = str(request.get_json().get("firstname"))
    lastname = str(request.get_json().get("lastname"))
    

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    SELECT firstname, lastname, grade, player_id 
                    FROM players 
                    WHERE firstname LIKE ? AND lastname LIKE ? AND is_minister = 0;
                    """, (firstname + "%", lastname + "%", ))
        players = cur.fetchall()
        

    return jsonify(players=players)



@teachers_bp.route("/teachers/pay_student_salary", methods=["POST"])
@check_authorization
def pay_salary(sub=None, role=None):
    salary = int(request.get_json().get("salary"))
    player_id = int(request.get_json().get("player_id"))


    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor();

        cur.execute("""
                    SELECT tax_paid 
                    FROM players 
                    WHERE player_id = ?;
                    """, (player_id, ))
        tax_paid = cur.fetchone()[0]
        if not tax_paid:
            salary -= salary * 0.1
            salary = ceil(salary)
        
        cur.execute("""
                    UPDATE players 
                    SET balance = balance + ?, tax_paid = 1
                    WHERE player_id = ?;
                    """, (salary, player_id, ))
        
        con.commit()
        

    return jsonify(salary=salary)
    


@teachers_bp.route("/teachers/pay_student_taxes", methods=["POST"])
@check_authorization
def pay_student_taxes(sub=None, role=None):
    player_id = int(request.get_json().get("player_id"))


    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        cur.execute("""
                    UPDATE players 
                    SET tax_paid = 1 
                    WHERE player_id = ?;
                    """, (player_id, ))
        
        con.commit()

    return "200"