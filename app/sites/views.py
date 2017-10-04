from flask import flash, redirect, render_template, url_for,session
from flask_login import login_required, login_user, logout_user

import datetime
from ..admin.views import check_admin
from . import sites
from forms import SurveyForm,ConfirmForm
from .. import db
from ..models import Site,Agent

@sites.route('/surveys', methods=['GET','POST'])
@login_required
def list_surveys():
    """
    List all site surveys
    """
    check_admin()

    survey_list = Site.query.all()
    current_date=datetime.datetime.now()

    return render_template('admin/sites/surveys.html',
                           surveys=survey_list,current_date=current_date, title="Surveys")


@sites.route('/survey/add', methods=['GET', 'POST'])
def add_survey():
    """
    Add a survey
    """
    check_admin

    form = SurveyForm()
    if form.validate_on_submit():
        survey = Site(business_name=form.business_name.data,
                            agent_name=form.agent_name.data,
                            phone_number=form.phone_number.data,
                            site_location=form.site_location.data,
                            latitude=form.latitude.data,
                            longitude=form.longitude.data,
                            business_type=form.business_type.data,
                            competing_products=form.competing_products.data,
                            upload_sketch=form.upload_sketch.data,
                            power_management=form.power_management.data,
                            time_spent=form.time_spent.data,
                            no_of_users=form.no_of_users.data,
                            demographics=form.demographics.data,
                            internet_available=form.internet_available.data,
                            internet_connection=form.internet_connection.data,
                            device_security=form.device_security.data,
                            due_date=None,
                            wifi_coverage=form.wifi_coverage.data)

        #If agent exists then add agent id else add new agent to agents table and get the ID
        #agent = Agent(agent_name=form.agent_name.data,
                        #    phone_number=form.phone_number.data)

        # add employee to the database
        db.session.add(survey)
        db.session.commit()
        flash('You have successfully added a new site survey!')

        # redirect to the login page
        return redirect(url_for('sites.list_surveys'))

    # load registration template
    return render_template('admin/sites/add_survey.html', form=form, title='Survey')


def date_by_adding_business_days(from_date, add_days):
    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5: # sunday = 6
            continue
        business_days_to_add -= 1
    return current_date

@sites.route('/surveys/backhaul/<int:id>', methods=['GET', 'POST'])
def send_to_backhaul(id):
    """
    Send to backhaul - Change status to in progress and add 3 days to counter from date of sending
    """
    backhaul = Site.query.get_or_404(id)
    backhaul.status='In progress'
    backhaul.due_date = date_by_adding_business_days(datetime.datetime.now(), 3)
    db.session.commit()
    return redirect(url_for('sites.list_surveys'))

@sites.route('/surveys/confirm/<int:id>', methods=['GET', 'POST'])
def confirm_backhaul(id):
    """
    confirm a site survey
    """
    check_admin
    confirm = Site.query.get_or_404(id)
    form = ConfirmForm()
    if form.validate_on_submit():
        confirm_site=form.confirm_site.data
        if confirm_site == 'yes' :
            confirm.status='Approved'
            confirm.approved_backhaul=form.approved_backhaul.data.id
            confirm.comments=str(form.comment.data)
            db.session.add(confirm)
            db.session.commit()
            flash('You have successfully confirmed a site!')
        else:
            confirm.approved_backhaul=form.approved_backhaul.data.id
            confirm.status='Failed'
            confirm.comments=str(form.comment.data)
            db.session.commit()
            flash('This is a failed site!')

        # redirect to the login page
        return redirect(url_for('sites.list_surveys'))

    # load registration template
    return render_template('admin/sites/confirm_site.html', form=form, title='Survey')
