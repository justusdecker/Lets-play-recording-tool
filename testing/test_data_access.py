import pytest
from bin.data_access import *
import bin.data_access
from os import remove
from sys import _getframe as gf
from bin.data_access import CSVObj
from tests import Tests


TESTS = Tests(bin.data_access)

@pytest.fixture
def csvi() -> CSVObj:
    return CSVObj('test.csv')

def test_read_empty_csv():
    csv_read('test.csv')
    file_write('testing.md',f'> Test Success\n> {gf().f_code.co_name}')
    
    
def test_write_empty_csv():
    csv_write('test.csv',[])
    
def test_csv(csvi):
    csvi
    
def test_csv_create(csvi):
    C = csvi
    S = {
        'version': "LOL",
        'epsiode_path': "lalala",
        'tad_path': "nope",
        'name': "WhoAmI",
        'game_name': "meh",
        'episode_length': 123
    }
    C.create(checklist=LP_KEYS,**S)
    
def test_csv_create_non_existent_key(csvi):
    C = csvi
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

def test_csv_create_no_key(csvi):
    C = csvi
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
    
def test_csv_read(csvi):
    remove('test.csv')
    C = csvi
    with pytest.raises(IndexError):
        C.read(1)
def test_csv_update(csvi):
    if isfile('test.csv'): remove('test.csv')
    C = csvi
    
    S = {
        'version': "LOL",
        'epsiode_path': "lalala",
        'tad_path': "nope",
        'name': "WhoAmI",
        'game_name': "meh",
        'episode_length': 123
    }
    C.create(checklist=LP_KEYS,**S)
    
    S['version'] = 'HELLO'
    
    C.update(0,checklist=LP_KEYS,**S)
def test_csv_update_wrong_index(csvi):
    if isfile('test.csv'): remove('test.csv')
    C = csvi
    
    S = {
        'version': "LOL",
        'epsiode_path': "lalala",
        'tad_path': "nope",
        'name': "WhoAmI",
        'game_name': "meh",
        'episode_length': 123
    }
    C.create(checklist=LP_KEYS,**S)
    with pytest.raises(IndexError):
        C.update(1,checklist=LP_KEYS,**S)
def test_csv_non_existent_key(csvi):
    if isfile('test.csv'): remove('test.csv')
    C = csvi
    
    S = {
        'version': "LOL",
        'epsiode_path': "lalala",
        'tad_path': "nope",
        'name': "WhoAmI",
        'game_name': "meh",
        'episode_length': 123
    }
    C.create(checklist=LP_KEYS,**S)
    
    S['test'] = 'HELLO'
    
    with pytest.raises(IndexError):
        C.update(0,checklist=LP_KEYS,**S)