from flask import abort, flash, redirect, render_template, url_for,request
from flask_login import current_user, login_required

from ..admin.views import check_admin
from . import agents
from .. import db
from ..models import Agent


@agents.route('/agents', methods=['GET', 'POST'])
@login_required
def list_agents():
    """
    List all agents
    """
    check_admin()

    agents_list = Agent.query.all()

    return render_template('admin/agents/agents.html',
                           agents=agents_list, title="Agents")
