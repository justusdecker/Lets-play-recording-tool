import pytest
from bin.data_access import *

def test_read_empty_csv():
    csv_read('test.csv')
    
def test_write_empty_csv():
    csv_write('test.csv',[])
    
def test_csv():
    CSVObj('test.csv')
    
def test_csv_create():
    C = CSVObj('test.csv')
    S = {
        'version': "LOL",
        'epsiode_path': "lalala",
        'tad_path': "nope",
        'name': "WhoAmI",
        'game_name': "meh",
        'episode_length': 123
    }
    C.create(checklist=LP_KEYS,**S)