from __init__ import app, socketio, config


if __name__ == "__main__":
    socketio.run(
        app,
        host=config["HOST"],
        port=config["PORT"],
        debug=config["DEBUG"],
        allow_unsafe_werkzeug=True
    )
