import os
from application import app, socketio, config


if __name__ == "__main__":
    try:
        socketio.run(
            app,
            host=config["HOST"],
            port=config["PORT"],
            debug=config["DEBUG"],
            allow_unsafe_werkzeug=True
        )
    except Exception as e:
        print(e)
        os.system("pause")
