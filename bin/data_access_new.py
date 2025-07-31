from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
from bin.constants import *
from os.path import isfile, isdir
from os import mkdir

DB_URL = f"sqlite:///{ROOT}lprt_data.db" # Define the database URL

Base = declarative_base()

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

def on_start():
    cnef(AUDIO_FOLDER)
    cnef(FIXED_AUDIO_FOLDER)
    cnef(THUMBNAIL_FOLDER)
    cnef(VIDEO_FOLDER)
    cnef(TAD_FOLDER)
    cnef(TEMP_FOLDER)

    if not isfile(OBS_SETTINGS_PATH):
        json_write(OBS_SETTINGS_PATH,DEFAULT_OBS_SETTINGS)

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

class LetsPlays(Base):
    __tablename__ = 'letsplays'
    id = Column(Integer, primary_key=True)
    tad_path = Column(String)
    name = Column(String)
    game_name = Column(String)
    episode_length = Column(Integer)
    description_path = Column(String)

class Episodes(Base):
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True)
    lpid = Column(Integer,default=0)
    video_path = Column(String)
    audio_mic_path = Column(String)
    audio_desktop_path = Column(String)
    thumbnail_path = Column(String)
    thumbnail_frame = Column(Numeric)
    has_problem = Column(Integer)
    audio_mic_edit1_path = Column(String)
    audio_mic_edit2_path = Column(String)
    audio_desktop_edit1_path = Column(String)
    audio_desktop_edit2_path = Column(String)
    title = Column(String)
    upload_at = Column(String)
    final_video_path = Column(String)
    
engine = create_engine(DB_URL) # Create the engine echo prints the sql querys

# create the users table
Base.metadata.create_all(engine)

# create a session to manage the connection to the database
Session = sessionmaker(bind=engine)
session = Session()

class SQLAccess:
    
    def get_ep_by_id(lpid:int):
        return SQLAccess.read_episodes()[lpid].lpid
    
    def __cvtid(lpid) -> int:
        return SQLAccess.read_letsplays()[lpid].id
    
    def create_episode(lpid: int, video_path: str):
        data = Episodes(video_path=video_path, lpid=SQLAccess.__cvtid(lpid))
        session.add(data)
        session.commit()
        
    def create_letsplay(name: str,game_name: str,episode_length: int):
        data = LetsPlays(name=name,game_name=game_name,episode_length=episode_length)
        session.add(data)
        session.commit()
    
    def read_letsplays() -> list[LetsPlays]:
        return [letsplay for letsplay in session.query(LetsPlays).all()]
    
    def read_all_episodes() -> list[Episodes]:
        return [episodes for episodes in session.query(Episodes).all()]
    
    def read_episodes(lpid: int) -> list[Episodes]:
        return [episodes for episodes in session.query(Episodes).all() if episodes.lpid == SQLAccess.__cvtid(lpid)]
    
    def update_letsplay(lpid:int, episode_length: int):
        data = SQLAccess.read_letsplays()
        data[lpid].episode_length =  episode_length
        session.commit()
    
    def update_episodes(lpid: int, epid: int,
                        **kwargs):
        data = SQLAccess.read_episodes(lpid)[epid]
        for key in kwargs:
            if not hasattr(data ,key):
                raise NameError(f'The attribute: [{key}] does not exist!')
            data.__setattr__(key,kwargs[key])
            
        session.commit()
        
    def delete_letsplay(lpid:int):
        data = session.query(LetsPlays).all()[lpid]
        session.delete(data)

        while SQLAccess.read_episodes(lpid):

            SQLAccess.delete_episode(lpid,0)


        session.commit()
    
    def delete_episode(lpid: int, epid: int):
        data = session.query(Episodes).filter(SQLAccess.__cvtid(lpid) == Episodes.lpid).all()[epid]
        session.delete(data)
        session.commit()
        
    def get_lp_names():
        return [entry.name for entry in session.query(LetsPlays).all()]
    
    def get_lp_game_names():
        return [entry.game_name for entry in session.query(LetsPlays).all()]
    
    def get_lp_ids():
        return [entry.id for entry in session.query(LetsPlays).all()]
    
    def get_video_path(lpid: int, epid: int):
        return [entry.video_path for entry in session.query(Episodes).all() if entry.lpid == SQLAccess.__cvtid(lpid)][epid]
    
    def get_episode_ammount(lpid: int):
        return len([entry for entry in session.query(Episodes).all() if entry.lpid == SQLAccess.__cvtid(lpid)])