import os


def make_temp_folder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

    for file in os.listdir(path):
        os.remove(os.path.join(path, file))

    return path
