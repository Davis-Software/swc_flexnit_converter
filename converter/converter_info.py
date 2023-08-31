import subprocess

from application import config


HANDBRAKE = config.get("HANDBRAKE_PATH")


_DESTINATIONS = [
    "av_mp4",
    "av_mkv",
    "av_webm",
]
_DESTINATION_CONTAINERS = {
    "av_mp4": "mp4",
    "av_mkv": "mkv",
    "av_webm": "webm"
}
_ENCODERS = [
    "svt_av1",
    "svt_av1_10bit",
    "x264",
    "x264_10bit",
    "nvenc_h264",
    "x265",
    "x265_10bit",
    "x265_12bit",
    "nvenc_h265",
    "nvenc_h265_10bit",
    "mpeg4",
    "mpeg2",
    "VP8",
    "VP9",
]


def destinations():
    return _DESTINATIONS


def destination_container(destination: str):
    if destination not in _DESTINATIONS:
        raise ValueError(f"Invalid destination: {destination}")

    return _DESTINATION_CONTAINERS[destination]


def encoders():
    return _ENCODERS


def ask_handbrake(params: list):
    handbrake = subprocess.Popen(
        [
            HANDBRAKE,
            *params
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    output = []
    raw = handbrake.stdout.read().decode("utf-8").split("\n")

    for line in raw:
        if "Option not supported by encoder" in line:
            continue
        if line.startswith("    "):
            output.append(line.strip(" \r"))

    return output


def encoder_presets(encoder: str):
    if encoder not in _ENCODERS:
        raise ValueError(f"Invalid encoder: {encoder}")

    return ask_handbrake(["--encoder-preset-list", encoder])


def encoder_tunes(encoder: str):
    if encoder not in _ENCODERS:
        raise ValueError(f"Invalid encoder: {encoder}")

    return ask_handbrake(["--encoder-tune-list", encoder])


def encoder_profiles(encoder: str):
    if encoder not in _ENCODERS:
        raise ValueError(f"Invalid encoder: {encoder}")

    return ask_handbrake(["--encoder-profile-list", encoder])


def encoder_levels(encoder: str):
    if encoder not in _ENCODERS:
        raise ValueError(f"Invalid encoder: {encoder}")

    return ask_handbrake(["--encoder-level-list", encoder])
