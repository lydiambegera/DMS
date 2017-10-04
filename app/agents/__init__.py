from flask import Blueprint

agents = Blueprint('agents', __name__)

from . import views
