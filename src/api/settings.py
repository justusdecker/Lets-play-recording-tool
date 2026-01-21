
from src.api.errors import SingeltonInstanceRuleBreak
import yaml


DEFAULT_SETTINGS = {'lang':'EN'}

class Settings:
    _instance = None
    def __init__(self):
        raise SingeltonInstanceRuleBreak("This is a Singleton, invoke get_instance() instead!")

    @classmethod
    def get_instance(cls):
        if cls._instance == None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def load(self):
        with open('settings.cfg') as file:
            data = file.read()
        self.data = yaml.safe_load(data)
    
    def save(self):
        with open('settings.cfg', 'w') as file:
            file.write(yaml.safe_dump(self.data))
