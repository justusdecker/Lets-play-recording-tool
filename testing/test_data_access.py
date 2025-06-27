import pytest
from bin.data_access import *
from os import remove

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
    
def test_csv_create_non_existent_key():
    C = CSVObj('test.csv')
    S = {
        'version': "LOL",
        'epsiode_path': "lalala",
        'tad_path': "nope",
        'name': "WhoAmI",
        'game_name': "meh",
        'episode_length': 123,
        'imakey': 'hehehehe'
    }
    with pytest.raises(IndexError):
        C.create(checklist=LP_KEYS,**S)

def test_csv_create_no_key():
    C = CSVObj('test.csv')
    S = {
        'version': "LOL",
        'epsiode_path': "lalala",
        'tad_path': "nope",
        'name': "WhoAmI",
        'game_name': "meh",
        'duh': 'hehe'
    }
    with pytest.raises(KeyError):
        C.create(checklist=LP_KEYS,**S)
    
def test_csv_read():
    remove('test.csv')
    C = CSVObj('test.csv')
    with pytest.raises(IndexError):
        C.read(1)