
from bin.data_access import json_read

class ThumbnailGenerator:
    def __init__(self, filepath: str):
        self.data = json_read(filepath)