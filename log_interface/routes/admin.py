from flask import Blueprint, session, jsonify, send_file
from models.account_model import AccountModel

"""
Contains endpoints related to the admin account
"""

admin_blueprint = Blueprint('admin', __name__) 

@admin_blueprint.route("/delete_account/<int:account_id>", methods=['DELETE'])
def delete_account(account_id):
    """
    Removes the account specified by the account_id
    """
    try:
        session_user_id = session.get("user_id")
        if account_id == session_user_id:
            return jsonify({
                "status" : "error",
                "message" : "Can't delete currently logged in account"
            }), 403
        account = AccountModel.fetch_account_by_id(session_user_id)
        if account.is_admin():
            target_account = AccountModel.fetch_account_by_id(account_id)
            target_account.delete_account()
            return jsonify({
                "status" : "ok",
                "message" : account_id
            }), 200
        else:
            return jsonify({
                "status" : "unauthorised",
                "message" : account_id
            }), 401
    except:
        return jsonify({
            "status" : "error",
            "message" : "Account not found"
        }), 404

@admin_blueprint.route("/download_database", methods=['GET'])
def download_database():
    try:
        session_user_id = session.get("user_id")
        account = AccountModel.fetch_account_by_id(session_user_id)
        if account.is_admin():
            return send_file('../data/data.db', as_attachment=True)
        else:
            return jsonify({
                "status" : "unauthorised",
                "message" : session_user_id
            }), 401
    except FileNotFoundError:
        return jsonify({
                "status" : "unauthorised",
                "message" : session_user_id
            }), 404