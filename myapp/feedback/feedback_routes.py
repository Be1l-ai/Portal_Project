from flask import render_template, request, redirect, url_for, flash, session, g
from . import feedback_bp
from myapp.db import get_db

@feedback_bp.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        select_company = request.form.get('select_company', '')
        title = request.form["title"]
        feedback = request.form["feedback"]
        error = None
        if not feedback:
            error = "Feedback is required to submit."
            flash(error)
            
        else:
            db = get_db()
            db.execute(
                "INSERT INTO feedback (company_id, title, body) VALUES (?, ?, ?)",
                (select_company, title, feedback,)
            )
            db.commit()
            flash("Feedback submitted successfully!")
            return redirect(url_for("feedback.index"))
        
    if request.method == "GET":
       db = get_db()
       user_list = db.execute(
           "SELECT id, username FROM user"
       ).fetchall()
       error = None
       if user_list is None:
           error = "No users found."
           flash(error)
           
    return render_template("index.html", user_list=user_list)
        