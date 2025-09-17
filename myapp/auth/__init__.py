from flask import blueprints

auth_bp = blueprints.Blueprint('auth', __name__)

from . import auth