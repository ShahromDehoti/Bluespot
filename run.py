# run.py
from myphoto_app import create_app, socketio, db

app = create_app()
socketio.init_app(app)  # Initialize SocketIO with the app
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, debug=True)
