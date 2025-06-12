from app import socket

@socket.on("connect")
def connect():
    print("Connection Established with Client")

def send_notification():
    socket.emit("update_projects", {"message": "New projects data available"}, namespace="/")