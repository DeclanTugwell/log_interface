import eventlet 
eventlet.monkey_patch()
from app import init_db, initialise_app, socket
from routes import register_endpoints
import os

app = initialise_app()

if __name__ == '__main__':
    init_db(app)
    register_endpoints(app)
    port = int(os.getenv("PORT", 5000))  # Get the PORT environment variable or default to 5000
    socket.run(app, host="0.0.0.0", port=port)