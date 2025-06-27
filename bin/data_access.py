import json
import csv
from os.path import isfile

LP_KEYS = [
    'version',
    'epsiode_path',
    'tad_path',
    'name',
    'game_name',
    'episode_length'] 

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

def json_read(filepath : str) -> dict | list:
    with open(filepath, 'r') as f:
        return json.load(f)
    
class CSVObj:
    """
    The default csv object to inherit from.
    """
    def __init__(self, filepath: str):
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
    
    def create(self,checklist: list[str], **kwargs) -> None:
        self.__check_list(checklist, kwargs)
        self.data.append([kwargs[arg] for arg in kwargs])
        
    def read(self,id: int):
        return self.data[id] if id < len(self.data) and id <= 0 and isinstance(id,int) else None
    
    def update(self,id: int,checklist: list[str],**kwargs):
        self.__check_list(checklist, kwargs)
        self.__check_id(id)
        self.data[id] = kwargs
        
    def delete(self,id: int):
        self.__check_id(id)
        self.data.pop(id)
    
class LetsPlays:
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
    def __init__(self, filepath: str='letsplay.csv'):
        self.data = csv_read(filepath)
        for row in self.data:
            if len(row) != len(LP_KEYS):
                raise IndexError()
    def create(self, **kwargs) -> None:

        
        [kwargs[arg] for arg in kwargs]
        
        self.data.append()