from flask import blueprints

main_bp = blueprints.Blueprint('main', __name__)

from . import routes