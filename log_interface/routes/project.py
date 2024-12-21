from flask import Blueprint, session, jsonify, request
from models.project_model import ProjectModel

"""
Contains endpoints related to the project table
"""

project_blueprint = Blueprint('project', __name__) 

@project_blueprint.route("/create_project", methods=['POST'])
def add_project():
    """
    Creates a project object based on the data passed in during the POST request.
    Saves the entity within the project table of the database
    """
    try:
        data = request.get_json()
        project_name = data.get("projectName")
        account_id = session["user_id"]
        if (ProjectModel.fetch_project_by_project_name(project_name) is not None):
            return jsonify({
                'status' : 'error',
                'message': 'Project name taken'
             }), 409
        project_modal = ProjectModel.create_model_from_request(project_name, account_id)
        new_project = project_modal.create_project()
        print(new_project.project_id)
        return jsonify({
            'status': 'ok',
            'body' : str(new_project.project_id)
        }), 200
    except:
        return jsonify({
            'status' : 'error',
            'message': 'Error creating account'
        }), 401
    
@project_blueprint.route("/delete_project/<int:project_id>", methods=['DELETE'])
def delete_project(project_id):
    """
    Deletes the project within the project table based upon the project_id provided.
    """
    try:
        target_project = ProjectModel.fetch_project_by_id(project_id)
        target_project.populate()
        target_project.delete_associated_logs()
        target_project.delete_project()
        return jsonify({
            "status" : "ok",
            "message" : project_id
        }), 200
    except:
        return jsonify({
            "status" : "error",
            "message" : "Project not found"
        }), 404
        
