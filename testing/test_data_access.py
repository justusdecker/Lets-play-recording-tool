import pytest
from bin.data_access import *
def test_read_empty_csv():
    csv_read('test.csv')
def test_write_empty_csv():
    csv_write('test.csv',[])