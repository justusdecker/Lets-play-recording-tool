import json
import csv

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
LP_KEYS = [
    'version',
    'epsiode_path',
    'tad_path',
    'name',
    'game_name',
    'episode_length'] 
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