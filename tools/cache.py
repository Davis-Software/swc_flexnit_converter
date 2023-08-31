from __future__ import annotations
from models.file_model import File


class Cache:
    def __init__(self):
        self.__file_cache: list[File] = []
        self.__output_file_cache: File or None = None

    # ------------------------------ #
    #     File Cache Management      #
    # ------------------------------ #
    def add_file(self, file: File):
        self.__file_cache.append(file)

    def get_file(self, file_uuid: str) -> File:
        for file in self.__file_cache:
            if file.uuid == file_uuid:
                return file
        raise Exception("File not found in cache")

    def remove_file(self, file_uuid: str):
        self.__file_cache.remove(
            self.get_file(file_uuid)
        )

    def get_file_list(self) -> list[File]:
        return self.__file_cache

    def get_file_list_json(self) -> list[dict]:
        return [file.to_json() for file in self.__file_cache]

    def clear(self):
        self.__file_cache.clear()

    # ------------------------------ #
    #   Output File Cache Management #
    # ------------------------------ #
    def set_output_file(self, file: File):
        self.__output_file_cache = file

    def get_output_file(self) -> File:
        return self.__output_file_cache

    def remove_output_file(self):
        self.__output_file_cache = None

    def has_output_file(self) -> bool:
        return self.__output_file_cache is not None

    def get_output_file_json(self) -> dict:
        return self.__output_file_cache.to_json() if self.has_output_file() else None

    def clear_output(self):
        self.__output_file_cache = None
