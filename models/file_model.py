class File:
    def __init__(self, uuid, name, size, extension, path):
        self.uuid = uuid
        self.name = name
        self.size = size
        self.extension = extension
        self.path = path

    def to_json(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "size": self.size,
            "extension": self.extension
        }

    def __repr__(self):
        return f"File('{self.uuid}', '{self.name}'"
