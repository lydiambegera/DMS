
from flask import abort, flash, redirect, render_template, url_for,request
from flask_login import current_user, login_required

from ..admin.views import check_admin
from . import organization
from forms import OrganizationForm
from .. import db
from ..models import Organization


@organization.route('/organization', methods=['GET', 'POST'])
@login_required
def list_organizations():
    """
    List all organizations
    """
    check_admin()

    organization_list = Organization.query.all()

    return render_template('admin/organization/organizations.html',
                           organizations=organization_list, title="Organizations")

@login_required
@organization.route('/organization/add', methods=['GET', 'POST'])
def add_organization():
    """
    Add an organization to the database
    """
    check_admin()
    form = OrganizationForm()
    if form.validate_on_submit():
        org_data = Organization(name=form.name.data,
                                    description=form.description.data)
        try:
            db.session.add(org_data)
            db.session.commit()
            flash('You have successfully added a new organization.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        return redirect(url_for('organization.list_organizations'))

    add_organization = True
    return render_template('admin/organization/add_organization.html', action="Add",
                               add_organization=add_organization, form=form,
                               title="Add Organization")

@organization.route('/organization/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_organization(id):
    """
    Edit an organization
    """
    check_admin()

    add_organization = False

    organization = Organization.query.get_or_404(id)
    form = OrganizationForm(obj=organization)
    if form.validate_on_submit():
        organization.name = form.name.data
        organization.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the organization.')

        # redirect to the departments page
        return redirect(url_for('organization.list_organizations'))

    form.description.data = organization.description
    form.name.data = organization.name
    return render_template('admin/organization/add_organization.html', action="Edit",
                           add_organization=add_organization, form=form,
                           organization=organization, title="Edit Organization")

@organization.route('/organization/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_organization(id):
    """
    Delete a department from the database
    """
    check_admin()

    organization = Organization.query.get_or_404(id)
    db.session.delete(organization)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_organizations'))

    return render_template(title="Delete organization")
