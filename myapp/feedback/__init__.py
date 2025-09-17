from flask import blueprints


feedback_bp = blueprints.Blueprint('feedback', __name__)

from . import feedback_routes