# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField, ValidationError,SelectMultipleField,TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from ..models import Site, Agent,Organization,Backhaul

class SurveyForm(FlaskForm):
    """
    Form for users to create new account
    """
    business_name = StringField('Business name', validators=[DataRequired()])
    site_location = StringField('Site location', validators=[DataRequired()])
    organization_id = QuerySelectField('Organization name',query_factory=lambda: Organization.query.all(),
                                  get_label="name")
    # option of adding a new organization or new agent
    agent_name = StringField('Agent name', validators=[DataRequired()])
    phone_number = StringField('Phone number', validators=[DataRequired()])
    latitude = StringField('Latitude', validators=[DataRequired()])
    longitude = StringField('Longitude', validators=[DataRequired()])
    business_type = StringField('Business type', validators=[DataRequired()])
    competing_products = StringField('Competing products', validators=[DataRequired()])
    upload_sketch = StringField('Upload sketch', validators=[DataRequired()])
    power_management = SelectField('Power access and management', validators=[DataRequired()],
                                                                    choices=[('agent', 'From agent'), ('solar', 'Solar panel required')])
    time_spent = SelectField('Time spent by users at location ', validators=[DataRequired()],
                                                                    choices=[('15','0-15 min'),('30','15-30 min'),('60','30-60 min'),('more','1 hr +')])
    no_of_users = SelectField('No of users at location', validators=[DataRequired()],
                                                            choices=[('50','0-50'),('100','50-100'),('150','100-150'),('more','More')])
    demographics = SelectField('Area demographics', validators=[DataRequired()],
                                                      choices=[('17','12-17 yrs'),('34','18-34 yrs'),('more','34 + yrs')])
    internet_available = SelectField('Internet available?', validators=[DataRequired()],
                                                             choices=[('yes','Yes'),('no','No')])
    internet_connection = SelectField('Internet connection type', validators=[DataRequired()],
                                                                    choices=[('fibre','Fibre'),('gsm','GSM')])
    device_security = SelectField('Device and equipment security', validators=[DataRequired()],
                                                                        choices=[('excellent','Excellent'),('good','Good'),('poor','Poor')])
    wifi_coverage = StringField('Wifi area coverage', validators=[DataRequired()])

    submit = SubmitField('Add')

class ConfirmForm(FlaskForm):
    """ Form to comfirm surveyed site to system """
    approved_backhaul = QuerySelectField('Backhaul name',query_factory=lambda: Backhaul.query.all(),
                                  get_label="backhaul_name")
    confirm_site = SelectField('Confirm site?', validators=[DataRequired()],
                                                                     choices=[('yes','Yes'),('no','No')])
    comment=TextAreaField()

    submit = SubmitField('Confirm')
