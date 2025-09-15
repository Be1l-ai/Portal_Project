import os
from flask import Flask, render_template
from flask import session, g
from myapp.db import get_db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',  # change this in production
        DATABASE = os.path.join(app.instance_path, 'flask.sqlite')
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # import and register blueprints from the main/ 
    from myapp.main import main_bp
    app.register_blueprint(main_bp)
    
    from . import db
    db.init_app(app)
    
    @app.before_request
    def load_logged_in_user():
        user_id = session.get("user_id")

        if user_id is None:
            g.user = None
        else:
            g.user = get_db().execute(
                "SELECT * FROM user WHERE id = ?", (user_id,)
            ).fetchone()
    
    return app

    

