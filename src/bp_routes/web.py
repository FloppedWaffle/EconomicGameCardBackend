from flask import Blueprint, request, jsonify, render_template
import sqlite3
from .func_utils import logger, SQLITE_PATH

web_bp = Blueprint("web", __name__)

@web_bp.route("/profile")
def get_index():
    return render_template("hello.html")


# @web_bp.route("/profile/get_balance", methods=["POST"])
# def get_balance():
