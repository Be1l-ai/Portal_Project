from flask import render_template, request, redirect, url_for, flash, session, g
from . import feedback_bp
from myapp.db import get_db

@feedback_bp.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        company_id = request.form["company_id"]
        title = request.form["title"]
        feedback = request.form["feedback"]
        error = None
        if not feedback:
            error = "Feedback is required to submit."
            
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO feedback (company_id, title, body) VALUES (?, ?, ?)",
                (company_id, title, feedback,)
            )
            db.commit()
            flash("Feedback submitted successfully!")
            return redirect(url_for("feedback.index"))
    return render_template("index.html")