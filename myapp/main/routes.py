from flask import render_template, request, redirect, url_for, flash, session, g
from . import main_bp
from myapp.db import get_db
from myapp.utils import login_required

# a simple page that says hello
@main_bp.route("/mainpage", methods=["GET"])
@login_required
def mainpage():
    return render_template('main/mainpage.html')

@main_bp.route("/dashboard")
@login_required
def dashboard():
    if request.method == "GET":
        db = get_db()
        feedback_list = db.execute(
            "SELECT title, company_id, created, body FROM feedback ORDER BY created DESC"
        ).fetchall()
        error = None
        if feedback_list is None:
            error = "No feedback found."
        if error is not None:
            flash(error)

    return render_template("main/dashboard.html",  feedback_list=feedback_list)


# things to change
#1st is the security -- dont know how to fix this for now -- still not fixed
#2nd is redirects -- fixed
#3rd is the code placement -- fixed
#4th is the front end
#5th i think the database is messed up? -- fixed