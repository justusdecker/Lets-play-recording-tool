import json
import csv
from bin.constants import LP_KEYS

def csv_read(filepath : str) -> list[list[str]]:
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
    def __init__(self):
        pass
    def create(self, **kwargs) -> None:
        [kwargs[arg] for arg in kwargs]
        self.data.append()
    def read(self,id: int):
        pass
    def update(self,id: int,**kwargs):
        pass
    def delete(self,id: int):
        pass
    
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