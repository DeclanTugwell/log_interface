from flask import Flask
from .login import login_blueprint
from .dashboard import dashboard_blueprint
from .admin import admin_blueprint
from .project import project_blueprint
from .log import log_blueprint

def register_endpoints(app: Flask):
    """
    Registers all the endpoints used within the application based on the respective blueprints 
    """
    app.register_blueprint(login_blueprint)
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(project_blueprint)
    app.register_blueprint(log_blueprint)