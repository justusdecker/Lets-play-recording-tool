from os.path import isfile, isdir
from os import mkdir, remove
import json
import csv

from typing import Any

def try_delete_file(filepath: str | None) -> bool:
    if filepath is not None:
        if isfile(filepath):
            remove(filepath)
            return True
    return False

def rie(filepath: str) -> None:
    """ remove if exist """
    if isfile(filepath):
        remove(filepath)

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

def csv_write(filepath: str, data: list[Any]):
    """
    Writes a Python list to a file in CSV format.

    This function overwrites the file if it already exists.
    """
    with open(filepath,'w',newline="") as f:
              
        w = csv.writer(f,delimiter='|',)
        w.writerows(data)

def csv_read(filepath: str) -> list[str]:
    """Reads JSON data from a file and parses it into a Python list."""
    with open(filepath,'r',newline="") as f: 
        w = csv.reader(f,delimiter='|',)
        return [row for row in w]

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