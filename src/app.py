import sqlite3
import sys
from flask import Flask, jsonify, request

from bp_routes.teachers import teachers_bp
from bp_routes.companies import companies_bp
from bp_routes.bankers import bankers_bp
from bp_routes.atm import atm_bp
from bp_routes.web import web_bp
from bp_routes.func_utils import SQLITE_PATH, get_auth_token, logger


app = Flask(__name__, template_folder='html')
app.register_blueprint(teachers_bp)
app.register_blueprint(companies_bp)
app.register_blueprint(bankers_bp)
app.register_blueprint(atm_bp)
app.register_blueprint(web_bp)


@app.route('/auth', methods=['POST'])
def authorize_user():
    password = request.get_json().get('auth_password')

    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()
        role = "teacher"

        cur.execute("""
                    SELECT teacher_id 
                    FROM teachers 
                    WHERE password = ?;
                    """, (password, ))
        user = cur.fetchone()

        if not user:
            role = "company"

            cur.execute("""
                        SELECT company_id 
                        FROM companies 
                        WHERE password = ?;
                        """, (password, ))
            user = cur.fetchone()

        if not user:
            role = "banker"

            cur.execute("""
                        SELECT banker_id 
                        FROM bankers 
                        WHERE password = ?;
                        """, (password, ))
            user = cur.fetchone()
        
        if not user:
            role = "atm"

            cur.execute("""
                        SELECT atm_id 
                        FROM atm 
                        WHERE password = ?;
                        """, (password, ))
            user = cur.fetchone()

        if not user:
            return "401", 401

    token = get_auth_token(password, role)
    if sys.version_info.minor < 10:
        token = token.decode("utf-8")
    
    if role == "teacher":
        logger.info(f"Учитель с id {user} вошёл в программу")
    elif role == "company":
        logger.info(f"Фирма с id {user} вошла в программу")
    elif role == "banker":
        logger.info(f"Банкир с id {user} вошёл в программу")
    else:
        logger.info(f"Банкомат с id {user} вошёл в программу")
        
    return jsonify(role=role, auth_token=token)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)