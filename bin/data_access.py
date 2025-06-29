import json
import csv
from os.path import isfile

LP_KEYS = [
    'version',
    'episode_path',
    'tad_path',
    'name',
    'game_name',
    'episode_length'] 

EP_KEYS = [
    'video_path',
    'audio_mic_path',
    'audio_desktop_path',
    'thumbnail_path',
    'thumbnail_frame'
]

def csv_rw(filepath: str, new_data):
    old_data = csv_read(filepath)
    csv_write(filepath, old_data + new_data)

def csv_read(filepath : str) -> list[list[str]]:
    if not isfile(filepath): return []
    with open(filepath,newline='') as f:
        reader = csv.reader(f, delimiter='|')
        return [row for row in reader]

def csv_write(filepath : str,data : list) -> None:
    with open(filepath,'w',newline='') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerows(data)

def file_read(filepath : str) -> str:
    with open(filepath, 'r') as f:
        return f.read()

def file_write(filepath : str, data : str):
    with open(filepath, 'w') as f:
        f.write(data)
        
def file_append(filepath : str, data : str):
    with open(filepath, 'a') as f:
        f.write(data)

def json_read(filepath : str) -> dict | list:
    with open(filepath, 'r') as f:
        return json.load(f)
    
class CSVObj:
    """
    The default csv object to inherit from.
    """
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = csv_read(filepath)
        for row in self.data:
            if len(row) != len(LP_KEYS):
                raise IndexError()
    def __check_list(self,cl:list[str],**kwargs):
        """
        checks list with a check list :o
        """
        if len(cl) != len(kwargs):
            raise IndexError(f'Length of a != b')
        for e in cl:
            if e not in kwargs:
                raise KeyError(f'cannot find: {e} in {kwargs}')
    
    def __check_id(self,id: int):
        if id >= len(self.data) or id > 0:
            raise IndexError()
        if not isinstance(id,int):
            raise TypeError()
    
    def save(self):
        csv_write(self.filepath, self.data)
    
    def create(self,checklist: list[str], **kwargs) -> None:
        self.__check_list(cl=checklist, **kwargs)
        self.data.append([kwargs[arg] for arg in kwargs])
        
    def read(self,id: int):
        self.__check_id(id)
        return self.data[id]
    
    def update(self,id: int,checklist: list[str],**kwargs):
        self.__check_list(cl=checklist, **kwargs)
        self.__check_id(id)
        self.data[id] = kwargs
        
    def delete(self,id: int):
        self.__check_id(id)
        self.data.pop(id)
    @property
    def row(self) -> int:
        return len(self.data)
    @property
    def col(self) -> int:
        if not self.data:
            return 0
        return len(self.data[0])

class LetsPlay(CSVObj):
    """
    
    |KEY|Type|
    |---|----|
    |Version|`str`|
    |episode_path|`str`|
    |tad_path|`str`|
    |name|`str`|
    |game_name|`str`|
    |episode_length|`int`|
    
    """
    def __init__(self, filepath):
        super().__init__(filepath)
    def create(self, **kwargs):
        return super().create(LP_KEYS, **kwargs)
    def update(self, id, **kwargs):
        return super().update(id, LP_KEYS, **kwargs)
    
    def get_episode_path(self,id: int) -> str:
        return self.read(id)[1]
    
    def get_name(self,id: int) -> str:
        return self.read(id)[4]
    
    def get_names(self) -> list[str]:
        return [i[4] for i in self.data]
    
    def get_episode_ammount(self) -> list[int]:
        return [Episode(i[1]).row for i in self.data]
    def get_episodes(self,id) -> list[int]:
        return Episode(self.read(id)[1])
class Episode(CSVObj):
    """
    
    !Must be added!
    
    """
    def __init__(self, filepath):
        super().__init__(filepath)
    def create(self, **kwargs):
        return super().create(EP_KEYS, **kwargs)
    def update(self, id, **kwargs):
        return super().update(id, EP_KEYS, **kwargs)