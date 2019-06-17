from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from DbClass import Database

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

conn = Database(app, 'mct', 'mct', 'solarweatherstation')


@app.route('/')
def hallo():
    return "Server is running"


@socketio.on("connect")
def connecting():
    socketio.emit("connected")
    print("Connection with client established")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")