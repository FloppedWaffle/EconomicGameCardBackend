import sqlite3
from functools import wraps
from flask import request
from datetime import datetime, timedelta, timezone
import jwt
import logging
import os

LOG_FILE = "history.log"
HASH_ALGO = "HS256"
secret = os.environ.get("FLASK_SECRET_WORD")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_PATH = os.path.join(BASE_DIR, "..", "..", "data", "payments.sqlite")


logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    level=logging.DEBUG,
    datefmt='%d.%m.%Y %H:%M:%S'
)
logger = logging.getLogger('rest_logger')




def get_auth_token(password: str, role: str) -> str:
    current_time = datetime.now(tz=timezone.utc)
    token = jwt.encode(
        {
            "sub": password,
            "role": role,
            "iat": current_time.timestamp(),
            "exp": (current_time + timedelta(hours=12)).timestamp()
        },
        secret,
        algorithm=HASH_ALGO)
    return token


def check_authorization(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return "401", 401
        try:
            payload = jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.exceptions.PyJWTError as e:
            logger.warning(str(e) + " (ошибка авторизации токена)")
            return "401", 401

        return f(*args, sub=payload["sub"], role=payload["role"], **kwargs)

    return wrapper



def pass_period():
    # TODO: Каждый час, каждый период нужно переносить профит (домноженный на 0.1) на налоги у частных фирм
    # TODO: Каждый час, каждый период нужно обнулять налоги всем игрокам, кроме гос. министров, владельцев и работников фирм
    # TODO: Каждый час, каждый период нужно обнулять is_minister_paid, чтобы министры могли брать зарплату


    with sqlite3.connect(SQLITE_PATH) as con:
        cur = con.cursor()

        # обнуляем налоги
        cur.execute("""
                    UPDATE players
                    SET tax_paid = 0
                    WHERE is_founder = 0 AND is_minister = 0 AND company_id = 0;
                    """)
        
        # обнуляем статус выдачи зарплаты министрам
        cur.execute("""
                    UPDATE players
                    SET is_minister_paid = 0
                    WHERE is_minister = 1;
                    """)
        
        # переносим десятую часть дохода на налоги, а доход обнуляем
        cur.execute("""
                    UPDATE companies
                    SET taxes = taxes + profit * 0.1, profit = 0
                    WHERE is_state = 0;
                    """)