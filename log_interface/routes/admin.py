from flask import Blueprint, session, jsonify
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
        if account_id == session["user_id"]:
            return jsonify({
                "status" : "error",
                "message" : "Can't delete currently logged in account"
            }), 403
        target_account = AccountModel.fetch_account_by_id(account_id)
        target_account.delete_account()
        return jsonify({
            "status" : "ok",
            "message" : account_id
        }), 200
    except:
        return jsonify({
            "status" : "error",
            "message" : "Account not found"
        }), 404