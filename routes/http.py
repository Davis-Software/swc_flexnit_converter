import os
import uuid

from application import app, socketio, cache, TEMP_FOLDER
from models.file_model import File

from flask import request, send_file, redirect, render_template


@app.route("/")
def index():
    return redirect("/av-conv")


@app.route("/av-conv")
def av_conv():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    file = request.files.get("file")
    file_uuid = str(uuid.uuid4())
    file_type = file.filename.split(".").pop()
    file_name = f"{file_uuid}.{file_type}"
    file_location = os.path.join(TEMP_FOLDER, file_name)

    file_model = File(
        file_uuid,
        file.filename,
        request.content_length,
        file_type,
        file_location
    )

    file.save(file_location)
    cache.add_file(file_model)

    socketio.emit("files", cache.get_file_list_json())
    return file_model.to_json()


@app.route("/download", methods=["GET"])
def download():
    file = cache.get_output_file()

    if file is None:
        return "No output file available"

    return send_file(
        file.path,
        as_attachment=True,
        download_name=file.name
    )
