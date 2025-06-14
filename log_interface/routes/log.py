from flask import Blueprint, jsonify, request, session
from models.log_model import LogModel
from datetime import datetime
from enums.log_type import LogType
from services.database_notification_service import send_notification

"""
Contains endpoints related to the log table
"""

log_blueprint = Blueprint('log', __name__) 

@log_blueprint.route("/create_log", methods=['POST'])
def add_log():
    """
    Creates a log entry using the data provided in the post request
    """
    try:
        if (session["user_id"] is not None):
            data = request.get_json()
            message = data.get("message")
            logType = LogType(int(data.get("logType")))
            timestamp = data.get("timestamp")
            session_id = data.get("sessionId")
            if timestamp == "":
                timestamp = datetime.now()
            log_model = LogModel.create_from_request(session_id, message, timestamp, logType)
            log_model.create_log()

            return jsonify({
                'status': 'ok',
                'body' : "Log created"
            }), 200
        else:
            return jsonify({
                'status': 'unauthorised',
                'body' : "Log not created"
            }), 401
    except:
        return jsonify({
            'status' : 'error',
            'message': 'Error creating log'
        }), 401
    
@log_blueprint.route("/delete_log/<int:log_id>", methods=['DELETE'])
def delete_log(log_id):
    """
    Deletes a log entry from the log table based on the log id
    """
    try:
        if (session["user_id"] is not None):
            target_log = LogModel.fetch_log_by_id(log_id)
            target_log.delete_log()
            send_notification()
            return jsonify({
                "status" : "ok",
                "message" : log_id
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
    
@log_blueprint.route("/get_logs/<int:project_id>", methods=['GET'])
def get_logs(project_id):
    """
    Fetches all logs associated with a project from the log table and returns them in JSON format
    """
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
                'body' : "Log not fetched"
            }), 401
    except:
        return jsonify({
            "status" : "error",
            "message" : "Log not found"
        }), 404

@log_blueprint.route('/update_log_type/<int:log_id>', methods=['UPDATE']) 
def update_log_type(log_id): 
    """
    Updates the log type of the log entry associated with the log_id
    """
    try:
        if (session["user_id"] is not None):
            data = request.get_json() 
            new_type = LogType(data.get("logType"))
            log = LogModel.fetch_log_by_id(log_id)
            log.update_type(new_type)
            return jsonify(
                    {
                        "status" : "ok",
                        "message" : "log updated"
                    }), 200
        else:
            return jsonify({
                'status': 'unauthorised',
                'body' : "Log not updated"
            }), 401
    except:
        return jsonify({
            "status" : "error",
            "message" : "Log not found"
        }), 404
