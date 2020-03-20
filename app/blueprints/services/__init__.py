from flask import Blueprint
bp = Blueprint('services', __name__)


from app.blueprints.services import routes
