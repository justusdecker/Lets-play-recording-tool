__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.3.114"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

import json
import csv
from os.path import isfile, isdir
from os import mkdir

from bin.constants import *

def csv_rw(filepath: str, new_data):
    """
    Reads existing data from a CSV file, appends new data to it, and then
    writes the combined data back to the same CSV file.

    This function effectively appends `new_data` to the end of the CSV file,
    preserving existing content. The CSV file is expected to use '|' as a delimiter.
    """
    old_data = csv_read(filepath)
    csv_write(filepath, old_data + new_data)

def csv_read(filepath : str) -> list[list[str]]:
    """
    Reads all data from a CSV file into a list of lists.

    Each inner list represents a row, and each element in the inner list
    is a string representing a cell value. The CSV file is expected to use
    '|' as a delimiter. If the file does not exist, an empty list is returned.
    """
    if not isfile(filepath): return []
    with open(filepath,newline='') as f:
        reader = csv.reader(f, delimiter='|')
        return [row for row in reader]

def csv_write(filepath : str,data : list) -> None:
    """
    Writes a list of lists to a CSV file.

    Each inner list in `data` is written as a row in the CSV file.
    The CSV file will use '|' as a delimiter. This function overwrites
    the file if it already exists.
    """
    with open(filepath,'w',newline='') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerows(data)

def isepisode_empty(filepath: str):
    """
    Checks if an 'Episode' object can be successfully instantiated from a given filepath.

    This function attempts to create an `Episode` object. If the instantiation
    succeeds (meaning the file contains valid episode data), it returns True.
    If any error occurs during instantiation (e.g., file not found, invalid format),
    it catches the exception and returns False.
    """
    try:
        e = Episode(ROOT + filepath)
        return True
    except:
        return False

def file_read(filepath : str) -> str:
    """Reads the entire content of a text file into a single string."""
    with open(filepath, 'r') as f:
        return f.read()

def file_write(filepath : str, data : str):
    """
    Writes a string to a text file.

    This function overwrites the file if it already exists.
    """
    with open(filepath, 'w') as f:
        f.write(data)
        
def file_append(filepath : str, data : str):
    """
    Appends a string to the end of a text file.

    If the file does not exist, it will be created.
    """
    with open(filepath, 'a') as f:
        f.write(data)

def json_read(filepath : str) -> dict | list:
    """Reads JSON data from a file and parses it into a Python dictionary or list."""
    with open(filepath, 'r') as f:
        return json.load(f)
    
def json_write(filepath : str, data : dict | list):
    """
    Writes a Python dictionary or list to a file in JSON format.

    This function overwrites the file if it already exists.
    """
    with open(filepath, 'w') as f:
        f.write(json.dumps(data))
   

def cnef(path: str):
    """
    Checks if a directory path exists, and if not, creates all necessary
    intermediate directories to ensure the full path exists.

    This function iterates through the components of the given path and
    creates each subdirectory if it doesn't already exist, effectively
    creating a nested directory structure.
    """
    if not isdir(path):
        sp = path.split('\\')
        for idx in range(len(sp)):
            if not idx: continue
            cp = "\\".join(sp[0:idx+1]) + '\\'
            if not isdir(cp):
                mkdir(cp)
class CSVObj:
    """
    A class for managing data stored in a CSV file, providing methods for
    reading, creating, updating, and deleting rows, with basic validation.

    This class treats the CSV file as a simple table where each row is a record.
    It enforces a strict column structure based on the provided `KEYS` dictionary
    during initialization. Data is loaded into memory upon instantiation and
    can be saved back to the file.
    """
    def __init__(self, filepath: str,KEYS: dict):
        """
        Reads existing data from the specified CSV file and performs an initial
        validation to ensure that each existing row has the same number of columns
        as defined by the `KEYS` dictionary. If a row's length does not match
        the expected number of keys, an `IndexError` is raised.
        """
        self.filepath = filepath
        self.data = csv_read(filepath)
        for row in self.data:
            if len(row) != len(KEYS):
                raise IndexError()
    def __check_list(self,cl:list[str],**kwargs):
        """
        Internal helper method to validate a list of keys against provided keyword arguments.

        Ensures that:
        1. The number of elements in `cl` (checklist) matches the number of
           keyword arguments provided.
        2. Every element in `cl` exists as a key in `kwargs`.

        This is used to validate input for `create` and `update` methods,
        ensuring that all required fields are present and correctly named.
        """
        if len(cl) != len(kwargs):
            raise IndexError(f'Length of a != b')
        for e in cl:
            if e not in kwargs:
                raise KeyError(f'cannot find: {e} in {kwargs}')
    
    def __check_id(self,id: int):
        """
        Internal helper method to validate a row ID.

        Ensures that:
        1. The `id` is an integer.
        2. The `id` is within the valid range of existing data rows.
        """
        if id >= len(self.data):
            raise IndexError()
        if not isinstance(id,int):
            raise TypeError()
    
    def save(self):
        """
        Saves the current in-memory data (`self.data`) back to the CSV file.

        This function overwrites the entire content of the file specified
        during initialization (`self.filepath`) with the current state of
        the `self.data` list.
        """
        csv_write(self.filepath, self.data)
    
    def create(self,checklist: list[str], **kwargs) -> None:
        """
        Appends a new row to the in-memory data.

        Validates the provided `kwargs` against `checklist` to ensure all
        required fields are present and correctly named. The values from
        `kwargs` are then appended as a new row to `self.data` in the order
        they appear in `kwargs`.
        """
        self.__check_list(cl=checklist, **kwargs)
        self.data.append([kwargs[arg] for arg in kwargs])
        
    def read(self,id: int):
        """
        Reads and returns a specific row from the in-memory data by its ID (index).

        Performs validation to ensure the ID is an integer and within valid bounds.
        """
        self.__check_id(id)
        return self.data[id]
    
    def update(self,id: int,checklist: list[str],**kwargs):
        """
        Updates a specific row in the in-memory data.

        Validates the provided `kwargs` against `checklist` and the `id`.
        The row at the given `id` is completely replaced by the values from `kwargs`.
        """
        self.__check_list(cl=checklist, **kwargs)
        self.__check_id(id)
        self.data[id] = kwargs
        
    def delete(self,id: int):
        """
        Deletes a specific row from the in-memory data.

        Performs validation to ensure the ID is an integer and within valid bounds.
        """
        self.__check_id(id)
        self.data.pop(id)
        
    @property
    def row(self) -> int:
        """Returns the number of rows (records) currently in the in-memory data."""
        return len(self.data)
    
    @property
    def col(self) -> int:
        """
        Returns the number of columns (fields) in the CSV data.

        If the data is empty, it returns 0. Otherwise, it returns the length
        of the first row, assuming all rows have a consistent number of columns.
        """
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
    |description_path|`str`|
    
    """
    def __init__(self, filepath):
        super().__init__(filepath,LP_KEYS)
    def create(self, **kwargs):
        return super().create(LP_KEYS, **kwargs)
    def update(self, id, **kwargs):
        return super().update(id, LP_KEYS, **kwargs)
    
    def get_episode_path(self,id: int) -> str:
        return self.read(id)[1]
    
    def get_game_name(self,id: int) -> str:
        return self.read(id)[3]
    
    def get_name(self,id: int) -> str:
        return self.read(id)[4]
    
    def get_description(self,id: int) -> str:
        return file_read(self.read(id)[6])
    
    def get_names(self) -> list[str]:
        return [i[4] for i in self.data]
    
    def get_episode_ammount(self) -> list[int]:
        return [Episode(ROOT + i[1]).row for i in self.data]
    def get_episodes(self,id) -> list:
        return Episode(ROOT + self.read(id)[1])
    def get_tad_path(self,id) -> list:
        return self.read(id)[2]

class Episode(CSVObj):
    """
    
    |id|key|type|
|---|---|---|
|0|video_path|`str`|
|1|audio_mic_path|`str`|
|2|audio_desktop_path|`str`|
|3|thumbnail_path|`str`|
|4|thumbnail_frame|`float`|
|5|has_problem|`bool`|
|6|audio_mic_edit1_path|`str`|
|7|audio_mic_edit2_path|`str`|
|8|audio_desktop_edit1_path|`str`|
|9|audio_desktop_edit2_path|`str`|
|10|title|`str`|
|11|episode_number|`int`|
|12|upload_at|`int`|
|12|final_video|`str`|
    
    """
    def __init__(self, filepath):
        super().__init__(filepath, EP_KEYS)
    def add(self,video_path: str):
        default = {i:'' for i in EP_KEYS}
        default['video_path'] = video_path
        self.create(**default)
    def create(self, **kwargs):
        return super().create(EP_KEYS, **kwargs)
    def update(self, id, **kwargs):
        return super().update(id, EP_KEYS, **kwargs)
    
    def get_video_path(self,id: int):
        return self.read(id)[0]
    def get_audio_mic_path(self,id: int):
        return self.read(id)[1]
    def get_audio_desktop_path(self,id: int):
        return self.read(id)[2]
    def get_thumbnail_path(self,id: int):
        return self.read(id)[3]
    def get_final_video_path(self,id: int):
        return self.read(id)[13]
    
    def get_audio_mic_edit1_path(self,id: int):
        return self.read(id)[6]
    def get_audio_mic_edit2_path(self,id: int):
        return self.read(id)[7]
    def get_audio_desktop_edit1_path(self,id: int):
        return self.read(id)[8]
    def get_audio_desktop_edit2_path(self,id: int):
        return self.read(id)[9]
    
    def set_audio_mic_edit1_path(self,id: int, data: str):
        self.read(id)[6] = data
    def set_audio_mic_edit2_path(self,id: int, data: str):
        self.read(id)[7] = data
    def set_audio_desktop_edit1_path(self,id: int, data: str):
        self.read(id)[8] = data
    def set_audio_desktop_edit2_path(self,id: int, data: str):
        self.read(id)[9] = data
    
    def set_audio_mic_path(self,id: int, data: str):
        self.read(id)[1] = data
    def set_audio_desktop_path(self,id: int, data: str):
        self.read(id)[2] = data
    def set_thumbnail_path(self,id: int, data: str):
        self.read(id)[3] = data
    def set_final_video_path(self,id: int, data: str):
        self.read(id)[13] = data
        
def check_lp_ep():
    lp = LetsPlay(LETS_PLAY_FILE_PATH)
    try:
        for i in range(lp.row):
            lp.get_episodes(i)
        return True
    except:
        return False
    
    
def on_start():
    cnef(AUDIO_FOLDER)
    cnef(FIXED_AUDIO_FOLDER)
    cnef(THUMBNAIL_FOLDER)
    cnef(VIDEO_FOLDER)
    cnef(TAD_FOLDER)
    cnef(TEMP_FOLDER)

    if not isfile(OBS_SETTINGS_PATH):
        json_write(OBS_SETTINGS_PATH,DEFAULT_OBS_SETTINGS)
    if not isfile(LETS_PLAY_FILE_PATH):
        csv_write(LETS_PLAY_FILE_PATH,[LP_KEYS])