import csv
from typing import Any
from bin.data_access import *
from sqlalchemy.sql import text



def test_read():
    data = csv_read('lets_play_export.csv')
    for desc, ep_len, lp_name, lpid, lp_gname, tad_path in data:
        print(desc, ep_len, lp_name, lpid, lp_gname, tad_path)

    data = csv_read('episodes_export.csv')
    for ep in data:
        print(ep)
