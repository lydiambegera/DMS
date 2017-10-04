from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,DateField,SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from datetime import date
from ..models import Site, Agent,Organization,User

class ScheduleForm(FlaskForm):
    """
    Form for admin to add or edit an Organization
    """
    installer = QuerySelectField('Installer name',query_factory=lambda: User.query.all(),
                                  get_label="username")
    no_devices = StringField('Number of devices to install', validators=[DataRequired()])
    schedule_date = DateField('Install date', format='%m/%d/%Y')
    submit = SubmitField('Submit')
