from flask import Blueprint
bp = Blueprint('subnets', __name__)


from app.blueprints.subnets import routes
