from flask import render_template, request, redirect, url_for, flash, session, g
from . import auth_bp
from myapp.db import get_db

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()
        
        if user is None:
            error = "Incorrect username."
        elif user["password"] != password:
            error = "Incorrect password."
        
        if error is not None:
            flash(error)
        else:
            session.clear() 
            session["user_id"] = user["id"] #is this safe??? --answer: supposedly yes but also no
            return redirect(url_for("main.mainpage"))
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        password = request.form["password"]
        username = request.form["username"]
        error = None
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
                
        if error is not None:
            flash(error)
        else:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, password),
                    #replace this shit with more secure shit later
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("feedback.index"))