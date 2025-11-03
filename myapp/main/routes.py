from flask import render_template, request, flash, session, g
from . import main_bp
from myapp.db import get_db
from myapp.utils import login_required

@main_bp.route("/mainpage", methods=["GET"])
@login_required
def mainpage():
    return render_template('main/mainpage.html')

@main_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard(): #add sorting system and search system
    if request.method == "GET":
        db = get_db()
        feedback_list = db.execute(
            "SELECT title, company_id, created, body FROM feedback WHERE company_id = ? ORDER BY created DESC",
            (session.get("user_id"),)
        ).fetchall()
        if not feedback_list:
            flash("No feedback found.")

    return render_template("main/dashboard.html",  feedback_list=feedback_list)

