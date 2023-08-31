import os

from application import socketio, cache

from converter import destinations, encoders, encoder_presets, encoder_tunes, encoder_profiles, encoder_levels, convert_file


@socketio.on("info")
def info():
    return cache.get_file_list_json()


@socketio.on("output")
def output():
    return cache.get_output_file_json()


@socketio.on("delete")
def delete(file_uuid):
    if file_uuid == "all":
        [os.remove(file.path) for file in cache.get_file_list()]
        cache.clear()
    elif file_uuid == "output":
        os.remove(cache.get_output_file().path)
        cache.clear_output()
    else:
        os.remove(cache.get_file(file_uuid).path)
        cache.remove_file(file_uuid)

    socketio.emit("files", info())
    socketio.emit("output", output())

    return info()


@socketio.on("destinations")
def get_destinations():
    return destinations()


@socketio.on("encoders")
def get_encoders():
    return encoders()


@socketio.on("encoder_presets")
def get_encoder_presets(encoder):
    return encoder_presets(encoder)


@socketio.on("encoder_tunes")
def get_encoder_tunes(encoder):
    return encoder_tunes(encoder)


@socketio.on("encoder_profiles")
def get_encoder_profiles(encoder):
    return encoder_profiles(encoder)


@socketio.on("encoder_levels")
def get_encoder_levels(encoder):
    return encoder_levels(encoder)


@socketio.on("convert")
def convert(data):
    convert_file(
        data["uuid"],
        data["destination"],
        data["encoder"],
        data["encoderPreset"],
        data["encoderTune"],
        data["encoderProfile"],
        data["encoderLevel"],
        data["quality"]
    )
    socketio.emit("output", output())
