from flask import flash, redirect, render_template, url_for,session
from flask_login import login_required, login_user, logout_user

import datetime
from ..admin.views import check_admin
from . import deployments
from forms import ScheduleForm
from .. import db
from ..models import Site,Agent

@deployments.route('/schedule', methods=['GET','POST'])
@login_required
def list_schedule_deployments():
    """
    List all site surveys
    """
    check_admin()

    schedule_list = Site.query.all()
    current_date=datetime.datetime.now()

    return render_template('admin/deployments/schedule_deployments.html',
                           schedule_list=schedule_list,current_date=current_date, title="Schedule deployments")
@login_required
@deployments.route('/schedule/add_schedule/<int:id>', methods=['GET', 'POST'])
def add_schedule(id):
    """
    Add an organization to the database
    """
    check_admin
    schedule = Site.query.get_or_404(id)
    #insert orders based on the number of devices put
    form = ScheduleForm()
    if form.validate_on_submit():
        devices = form.no_devices.data
        for device in devices :
            schedule.deployed_by=form.installer.data.id
            schedule.deployment_scheduled_date=form.schedule_date.data
            schedule.site_id=id
            db.session.add(schedule)
            db.session.commit()
        flash('You have successfully ordered a device for this site!')

        # redirect to the schedule list page
        return redirect(url_for('deployments.list_schedule_deployments'))

    # load registration template
    return render_template('admin/deployments/schedule.html', form=form, title='Survey')
