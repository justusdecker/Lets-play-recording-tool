from sqlalchemy import create_engine, text

from bin.constants import ROOT

import json

DB_URL = f"sqlite:///{ROOT}lprt_data.db" # Define the database URL

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
   
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

from sqlalchemy import create_engine, Column, Integer, String, Numeric

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
    
engine = create_engine(DB_URL, echo=True) # Create the engine echo prints the sql querys

# create the users table
Base.metadata.create_all(engine)

# create a session to manage the connection to the database
Session = sessionmaker(bind=engine)
session = Session()
    
