# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from ..models import  User , Organization

from . import admin
from .. import db

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)
# Employee Views

@admin.route('/users')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = User.query.all()
    return render_template('admin/users.html',
                           employees=employees, title='Users')
