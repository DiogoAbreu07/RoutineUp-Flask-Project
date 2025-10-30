from flask import Blueprint
hub_bp = Blueprint("hub", __name__, url_prefix="/home")
from . import routes  # noqa
