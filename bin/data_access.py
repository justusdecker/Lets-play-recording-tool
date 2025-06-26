import json
import csv

def csv_read(filepath : str):
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile)
        return [row for row in reader]
            

def file_read(filepath : str) -> str:
    with open(filepath, 'r') as f:
        return f.read()

def json_read(filepath : str) -> dict | list:
    with open(filepath, 'r') as f:
        return json.load(f)