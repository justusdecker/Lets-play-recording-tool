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
    
csv_write('test.csv',[[1,41,341,43],[1,41,341,43]])