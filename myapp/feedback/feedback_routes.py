from flask import render_template, request, redirect, url_for, flash, session, g
from . import feedback_bp
from myapp.db import get_db

@feedback_bp.route("/index", methods=["GET", "POST"])
def index():
    db = get_db()
    user_list = db.execute("SELECT id, username FROM user").fetchall()
    if request.method == "POST":
        select_company = request.form.get('select_company', '')
        title = request.form.get('title', '')
        feedback = request.form.get('feedback', '')
        error = None
        if not feedback:
            error = "Feedback is required to submit."
        elif not title:
            error = "Title is required to submit."
        elif len(title) < 5 or len(title) > 100:
            error = "Title must be between 5 and 100 characters long."
        elif not select_company:
            error = "You must select a company to submit feedback to."
        elif len(feedback) < 10 or len(feedback) > 5000:
            error = "Feedback must be between 10 and 5000 characters long."
        else:
            try:
                db.execute(
                    "INSERT INTO feedback (company_id, title, body) VALUES (?, ?, ?)",
                    (select_company, title, feedback,)
                )
                db.commit()
                flash("Feedback submitted successfully!")
                return redirect(url_for("feedback.index"))
            except Exception as e:
                error = f"Error: {e}"
        if error:
            flash(error)
        
    return render_template("index.html", user_list=user_list)
        