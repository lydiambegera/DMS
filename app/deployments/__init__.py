from flask import Blueprint

deployments = Blueprint('deployments', __name__)

from . import views
