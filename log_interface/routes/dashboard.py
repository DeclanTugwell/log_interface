from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from models.account_model import AccountModel
from models.project_model import ProjectModel

"""
Contains endpoints related to the dashboard page
"""

dashboard_blueprint = Blueprint('dashboard_page', __name__) 

@dashboard_blueprint.route("/dashboard")
def dashboard_page():
    """
    Fetches data to populate the dashboard template and then renders and returns it.
    """
    session_user_id = session.get("user_id")
    account = AccountModel.fetch_account_by_id(session_user_id)
    is_admin = account.is_admin()
    accounts = []
    if (is_admin):
        accounts = AccountModel.fetch_accounts()
    projects = account.fetch_associated_populated_projects()
    return render_template('dashboard.html', isAdmin=is_admin, username=session["username"], accounts=accounts, projects=projects)

@dashboard_blueprint.route("/logout", methods=["GET"])
def logout():
    """
    Used to end the logged in users session
    """
    try:
        session.pop("user_id", None)
        session.pop("username", None)
        return redirect(url_for('login_page.login_page'))
    except: 
        return jsonify({
            'status' : 'error',
            'message': 'Unable to log out'
        }), 401