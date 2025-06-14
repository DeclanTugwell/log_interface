from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from models.account_model import AccountModel
from werkzeug.security import generate_password_hash, check_password_hash

"""
Contains endpoints related to the login page
"""

login_blueprint = Blueprint('login_page', __name__) 

@login_blueprint.route("/")
def login_page():
    """
    Renders and returns the login page
    """
    return render_template('login.html')

@login_blueprint.route("/login", methods=['POST'])
def login():
    """
    Attempts to login a user based on the credentials provided.
    If successfull a session is created for the user.
    """
    matching_account = None
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    target_account = AccountModel.fetch_account_by_username(username)
    if (target_account is not None and check_password_hash(target_account.password, password) == True):
        matching_account = AccountModel(target_account)
    if (matching_account != None):
        session["user_id"] = matching_account.account_id
        session["username"] = matching_account.username
        return redirect(url_for('dashboard_page.dashboard_page'))
    else:
        print("Account not found")
    
    return jsonify({
        'status' : 'error',
        'message': 'Invalid username or password'
    }), 401

@login_blueprint.route("/register", methods=['POST'])
def register():
    """
    Attempts to register a user account based on the credentials passed in during the POST request.
    Validation is also performed to ensure the credentials meet the required standards.
    """
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        credential_issues = AccountModel.validate_username_password_entry(username, password)
        if(len(credential_issues) > 0):
            error_messages = [str(issue) for issue in credential_issues]
            output_message = "Password must contain: " + ", ".join(error_messages)
            return jsonify({
                'status' : 'error',
                'message' : output_message
            }), 403
        if (AccountModel.fetch_account_by_username(username) is not None):
            return jsonify({
                'status' : 'error',
                'message': 'Username already taken'
                }), 409
        hashed_password = generate_password_hash(password)
        account_service = AccountModel.from_registration(username, hashed_password, False)
        new_account = account_service.create_account()
        return jsonify({
            'status': 'ok',
            'body' : new_account.account_id
        }), 200
    except:
        return jsonify({
            'status' : 'error',
            'message': 'Invalid username or password'
        }), 401