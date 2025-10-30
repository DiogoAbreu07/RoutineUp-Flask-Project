from flask import Blueprint
reminders_bp = Blueprint("reminders", __name__, url_prefix="/reminders", template_folder="../../templates")
from . import routes  # noqa
