from flask import Blueprint, jsonify, request, session
from models.user_session_model import UserSessionModel
from models.project_user_model import ProjectUserModel
from services.database_notification_service import send_notification

project_user_blueprint = Blueprint('project_user_blueprint', __name__) 

@project_user_blueprint.route("/delete_project_user/<int:project_user_id>", methods=['DELETE'])
def delete_session(project_user_id):
    """
    Deletes a log session from the log sessions based on the log id
    """
    try:
        session_user_id = getattr(session, "user_id", None)
        if (session_user_id is not None):
            project_user = ProjectUserModel.fetch_project_user_by_project_user_id(project_user_id)
            project_user.delete_project_user()
            send_notification()
            return jsonify({
                "status" : "ok",
                "message" : project_user_id
            }), 200
        else:
            return jsonify({
                'status': 'unauthorised',
                'body' : "Session not deleted"
            }), 401
    except:
        return jsonify({
            "status" : "error",
            "message" : "Session not found"
        }), 404