from flask import render_template, request, redirect, url_for, flash, session, g
from . import main_bp
from myapp.db import get_db
from functools import wraps

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("main.login"))
        return view(**kwargs)
    return wrapped_view

# a simple page that says hello
@main_bp.route('/index')
def index():
    return render_template('index.html')
    
@main_bp.route("/mainpage")
@login_required
def mainpage():
    return render_template('mainpage.html')


@main_bp.route("/login", methods=["GET", "POST"])
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

@main_bp.route("/register", methods=["GET", "POST"])
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
                return redirect(url_for("main.login"))
    return render_template("auth/register.html")

@main_bp.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")


# things to change
#1st is the security -- dont know how to fix this for now
#2nd is redirects
#3rd is the code placement --supposedly its fine but i feel like its not
#4th is the front end
#5th i think the database is messed up? --update database fixed