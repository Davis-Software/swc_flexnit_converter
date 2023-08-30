import os
import uuid
import tempfile

from models.file_model import File

from __init__ import cache, config, socketio
from ffmpeg import FFmpeg


def convert_file(file_uuid, transcode_audio, transcode_video, accelerator, encoder_preset, output_format):
    ffmpeg = config.get("FFMPEG_PATH")
    hw_accel = config.get_bool("FFMPEG_NVENC")

    accelerator = accelerator if (accelerator in
                                  ["cuda", "nvdec", "vdpau", "vaapi"]
                                  ) else "cuda"
    encoder_preset = encoder_preset if (encoder_preset in
                                        ["slow", "medium", "fast", "hp", "hq", "bd", "ll", "llhq", "llhp", "lossless",
                                         "losslesshp"]
                                        ) else "slow"

    file = cache.get_file(file_uuid)

    if file is None:
        return

    output_name = ".".join(file.name.split(".")[:-1])
    if transcode_audio or transcode_video:
        output_name += "_tc_"
    if transcode_audio:
        output_name += "a"
    if transcode_video:
        output_name += "v"
    output_name += f".{output_format}"

    ffmpeg = FFmpeg(ffmpeg).option("y").option("loglevel", "quiet")

    if hw_accel:
        ffmpeg.option("hwaccel", accelerator)
        ffmpeg.option("hwaccel_output_format", "cuda")

    ffmpeg.input(file.path)

    opts = {}
    if not transcode_audio:
        opts["c:a"] = "copy"

    if not transcode_video:
        opts["c:v"] = "copy"
    else:
        opts["c:v"] = "h264_nvenc"
        opts["preset"] = encoder_preset

    file_uuid = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_uuid}.{output_format}")

    file = File(
        file_uuid,
        output_name,
        0,
        output_format,
        file_path
    )

    ffmpeg.output(file_path, opts)

    @ffmpeg.on("start")
    def ffmpeg_start(args):
        print(f"Converting - Start: {args}")

    @ffmpeg.on("progress")
    def ffmpeg_progress(progress):
        socketio.emit("progress", {
            "file_uuid": file_uuid,
            "progress": progress
        })
        print(f"Converting - Progress: {progress}%")

    @ffmpeg.on("stderr")
    def ffmpeg_error(error):
        print(f"Converting - Error: {error}")

    @ffmpeg.on("completed")
    def ffmpeg_completed():
        print("Converting - Finished")
        cache.set_output_file(file)
        socketio.emit("progress", {
            "file_uuid": file_uuid,
            "progress": 100
        })

    ffmpeg.execute()

    return file

