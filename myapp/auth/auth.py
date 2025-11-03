from flask import render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp
from myapp.db import get_db

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        error = None
        db = get_db()
        
        try:
            user = db.execute(
                "SELECT * FROM user WHERE username = ?", (username,)
            ).fetchone()
            
            if user is None:
                error = "Incorrect username."
            elif not check_password_hash(user["password"], password):
                error = "Incorrect password."
            
            else:
                session.clear()
                session["user_id"] = user["id"]
                return redirect(url_for("main.mainpage"))
        except Exception as e:
            error = f"Error: {e}"

        if error:
            flash(error)
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        password = request.form.get("password", "")
        username = request.form.get("username", "")
        error = None
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif len(password) < 8:
            error = "Password must be at least 8 characters long."
        elif len(username) < 3 or len(username) > 30:
            error = "Username must be between 3 and 30 characters long."
        else:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
                flash("Registration successful!")
                return redirect(url_for("auth.login"))
            except db.IntegrityError:
                error = f"User {username} is already registered."
        if error:
            flash(error)
    return render_template("auth/register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("feedback.index"))