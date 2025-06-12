from flask import Blueprint, jsonify, request, session
from models.log_model import LogModel
from models.account_model import AccountModel
from models.project_user_model import ProjectUserModel
from models.user_session_model import UserSessionModel
from enums.log_type import LogType
from werkzeug.security import check_password_hash
from datetime import datetime
from services.email_service import Email
from services.database_notification_service import send_notification

account_session_blueprint = Blueprint('account_session_blueprint', __name__) 

@account_session_blueprint.route("/create_session", methods=['POST'])
def add_session():
    try:
        data = request.get_json()
        project_id = data.get("projectId")
        hardware_id = data.get("hardwareId")
        log_list = data.get("logList")
        if (session.get("user_id") is not None):
            return create_session(project_id, hardware_id, log_list)
        else:
            username = data.get("username")
            password = data.get("password")
            target_account = AccountModel.fetch_account_by_username(username)
            if (target_account is not None and check_password_hash(target_account.password, password) == True and (target_account.is_admin() or target_account.is_associated_with_project(project_id))):
                return create_session(project_id, hardware_id, log_list)
            else:
                return jsonify({
                    'status': 'unauthorised',
                    'body' : "Log created"
                }), 401
    except:
        return jsonify({
            'status' : 'error',
            'message': 'Error creating log'
        }), 401
    
def create_session(project_id, hardware_id, log_list):
    target_user = ProjectUserModel.fetch_project_user_by_hardware_id(hardware_id)
    if (target_user is None):
        user_model = ProjectUserModel.create_model_from_request(hardware_id, project_id)
        target_user = user_model.create_project_user()
    user_session_model = UserSessionModel.create_model_from_request(target_user.user_id)
    user_session = user_session_model.create_user_session()

    for log in log_list:
        message = log["message"]
        log_type = LogType(int(log["logType"]))
        timestamp = log["timestamp"]
        if timestamp is None or timestamp == "":
            timestamp = datetime.now()
        else:
            timestamp = datetime.fromisoformat(timestamp)
        log_model = LogModel.create_from_request(user_session.session_id, message, timestamp, log_type)
        log_model.create_log()

    send_email_notification(user_session)
    send_notification()
    
    return jsonify({
                'status': 'ok',
                'body' : "Log created"
            }), 200

    
@account_session_blueprint.route("/delete_session/<int:session_id>", methods=['DELETE'])
def delete_session(session_id):
    """
    Deletes a log session from the log sessions based on the log id
    """
    try:
        if (session["user_id"] is not None):
            target_session = UserSessionModel.fetch_user_session_by_session_id(session_id)
            target_session.delete_user_session()
            send_notification()
            return jsonify({
                "status" : "ok",
                "message" : session_id
            }), 200
        else:
            return jsonify({
                'status': 'unauthorised',
                'body' : "Log created"
            }), 401
    except:
        return jsonify({
            "status" : "error",
            "message" : "Log not found"
        }), 404
    
@account_session_blueprint.route("/get_sessions/<int:project_id>", methods=['GET'])
def get_logs(project_id):
    try:
        if (session["user_id"] is not None):
            serialised_logs = []
            logs = LogModel.fetch_logs_by_session_id(project_id)
            for log in logs:
                serialised_logs.append(log.serialise())
            return jsonify(
                {
                    "status" : "ok",
                    "message" : "logs fetched successfully",
                    "data": serialised_logs
                }), 200
        else:
            return jsonify({
                'status': 'unauthorised',
                'body' : "Log created"
            }), 401
    except:
        return jsonify({
            "status" : "error",
            "message" : "Log not found"
        }), 404
    
def send_email_notification(session : UserSessionModel):
    session.populate()
    subject = ""
    if session.error_count > 0:
        subject = "ERROR"
    if session.event_count > 0:
        if subject != "":
            subject = subject + ", "
        subject = subject + "EVENT"
    if session.warning_count > 0:
        if subject != "":
            subject = subject + ", "
        subject = subject + "WARNING"
    if subject != "":
        contents = f"Error Count: {session.error_count}\nEvent Count: {session.event_count}\nWarning Count: {session.warning_count}\nInformation Count: {session.info_count}\n\nGG :)"
        email_service = Email()
        email_service.send(subject, contents)
