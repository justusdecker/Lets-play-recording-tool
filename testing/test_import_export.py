import csv
from typing import Any
from bin.data_access import *
    

def test_read():
    data = csv_read('lets_play_export.csv')
    for desc, ep_len, lp_name, lpid, lp_gname, tad_path in data:
        print(desc, ep_len, lp_name, lpid, lp_gname, tad_path)

    data = csv_read('episodes_export.csv')
    for ep in data:
        print(ep)
def test_write():
    from os import getlogin
    USERNAME = getlogin()
    del getlogin

    ROOT = f'C:\\Users\\{USERNAME}\\lprt\\'
    from shutil import copyfile
    from os import remove
    from sqlalchemy import create_engine, Column, Integer, String, Numeric
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    DB_URL = f"sqlite:///{ROOT}lprt_data.db"
        
    DB_PATH = f'{ROOT}lprt_data.db'
    copyfile(DB_PATH, DB_PATH + 'x') # <- create the backup. lprt.dbx
    remove(DB_PATH) # <- remove the original db
    #Create the db again
    Base = declarative_base()
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    

        
    data = LetsPlays(name=name, game_name=game_name, episode_length=episode_length)
    session.add(data)
    session.commit()