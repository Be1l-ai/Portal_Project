from flask import render_template
from . import main_bp

# a simple page that says hello
@main_bp.route('/index')
def index():
    return render_template('index.html')
    
@main_bp.route("/")
def is_working():
    return "The website is working!"
