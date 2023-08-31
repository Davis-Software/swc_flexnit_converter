import os
from application import socketio, cache

from converter import convert_file


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

    return info()


@socketio.on("convert")
def convert(file_uuid, transcode_audio, transcode_video, accelerator, encoder_preset, output_format):
    return convert_file(
        file_uuid,
        transcode_audio,
        transcode_video,
        accelerator,
        encoder_preset,
        output_format
    ).to_json()
