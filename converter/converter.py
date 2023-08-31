import os
import uuid
import subprocess

from models.file_model import File

from application import cache, socketio, TEMP_FOLDER
from .converter_info import HANDBRAKE, destination_container


def emit(channel, data):
    socketio.emit(channel, data)


def convert_file(
    file_uuid,
    container,
    encoder,
    encoder_preset,
    encoder_tune,
    encoder_profile,
    encoder_level,
    quality
):
    file = cache.get_file(file_uuid)

    if not file or not os.path.exists(file.path):
        raise FileNotFoundError(f"File {file_uuid} does not exist.")

    emit("state", "preparing")
    # clear for the socket queue to be sent
    socketio.sleep(.1)

    container_file = destination_container(container)
    file_uuid = str(uuid.uuid4())
    new_file = f"{file_uuid}.{container_file}"
    new_name = f"{file.name}-tc.{container_file}"

    destination_file = File(
        file_uuid,
        new_name,
        -1,
        container_file,
        os.path.join(
            TEMP_FOLDER,
            new_file
        )
    )

    handbrake_opts = [
        HANDBRAKE,
        "-i", file.path,
        "--main-feature",
        "-o", destination_file.path,
        "-f", container,
        "--no-markers",
        "-O",
        "--align-av",
        "-e", encoder
    ]

    if encoder_preset != "":
        handbrake_opts.extend(["--encoder-preset", encoder_preset])

    if encoder_tune != "":
        handbrake_opts.extend(["--encoder-tune", encoder_tune])

    if encoder_profile != "":
        handbrake_opts.extend(["--encoder-profile", encoder_profile])

    if encoder_level != "":
        handbrake_opts.extend(["--encoder-level", encoder_level])

    handbrake_opts.extend(["--quality", str(quality)])

    handbrake_opts.extend([
        "--all-audio",
    ])

    handbrake = subprocess.Popen(
        handbrake_opts,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    for stdout in handbrake.stdout:

        # HandBrake has exited
        if "HandBrake has exited" in stdout or len(stdout) == 0:
            break

        elif "Encoding: task" in stdout:
            progress = 0
            speed = -1
            eta = "tbd"

            try:
                progress = float(stdout.split(", ")[1].split(" %")[0])
            except:
                pass

            if "(" in stdout:
                try:
                    speed = float(stdout.split("(")[1].split(" fps")[0])
                except:
                    pass

                try:
                    eta = stdout.split("ETA ")[1].split(")[")[0]
                except:
                    pass

            emit("progress", {
                "progress": progress,
                "speed": speed,
                "eta": eta
            })
            # clear for the socket queue to be sent
            socketio.sleep(.1)

    emit("state", "normal")

    if cache.get_output_file():
        os.remove(cache.get_output_file().path)
        cache.clear_output()

    destination_file.size = os.path.getsize(destination_file.path)
    cache.set_output_file(destination_file)
