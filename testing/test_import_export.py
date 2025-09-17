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



from os import getlogin
    
USERNAME = getlogin()
del getlogin
from shutil import copyfile
from os import remove
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
def create_lps_from_csv():
    global session, engine
    #! This will be not included because the values exist in SQLAccess
    ROOT = f'C:\\Users\\{USERNAME}\\lprt\\'
    DB_URL = f"sqlite:///{ROOT}lprt_data.db"
    DB_PATH = f'{ROOT}lprt_data.db'
    
    
    # Close, Backup & Remove
    SQLAccess.close_and_dispose()
    SQLAccess.backup_and_remove()
    
    # Create the db again -> move inside its own function
    Base = declarative_base()
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    data = csv_read('lets_play_export.csv')

    SQLAccess.manually_recreate_lets_play(session)
    SQLAccess.import_lets_plays(session,data)
    

    data = csv_read('episodes_export.csv')
    
    SQLAccess.manually_recreate_episodes(session)
    SQLAccess.import_episodes(session, data)
    
    session.commit()