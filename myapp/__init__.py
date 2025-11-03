import os
from flask import Flask
from flask import session, g
from myapp.db import get_db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',  # no need to change not meant for production
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite')
    )
    if test_config is None:
        # no test config but when needed load the instance config
        app.config.from_pyfile('config.py', silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # import and register blueprints from the main/ and auth/ and feedback/
    from myapp.main import main_bp
    from myapp.auth import auth_bp
    from myapp.feedback import feedback_bp
    app.register_blueprint(main_bp, url_prefix="/main")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(feedback_bp, url_prefix="/feedback")
    
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

