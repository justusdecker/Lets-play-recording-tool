#from bin.welcome_popup import WELCOME
#from bin.translation import gtran
#WELCOME.update_message(f'{gtran("bin::welcome::load")} {__name__}')

from tkinter.messagebox import showerror
try:
    from sqlalchemy import create_engine, Column, Integer, String, Numeric
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.sql import text
except:
    from bin.constants import ERROR_008
    showerror('ERROR', ERROR_008 + '\nSQLAlchemy')
    quit()

import json
from bin.constants import *
from os.path import isfile, isdir
from os import mkdir, remove
from PIL import ImageTk, Image
import base64
from PIL import ImageTk, Image
from io import BytesIO
from shutil import copyfile
import sys
import csv
from typing import Any
from bin.xmsgbox import xerr
from datetime import datetime as dt
DB_PATH = f'{ROOT}lprt_data.db'

def try_delete_file(filepath: str | None) -> bool:
    if filepath is not None:
        if isfile(filepath):
            remove(filepath)
            return True
    return False

class AsciiImage:
    def __init__(self, var: str):
        self.var = var

        decoded_data =  base64.b64decode(var.encode('ascii'))
        io_stream = BytesIO(decoded_data)
        img = Image.open(io_stream)
        self.image = ImageTk.PhotoImage(img)

DB_URL = f"sqlite:///{ROOT}lprt_data.db" # Define the database URL

Base = declarative_base()

def rie(filepath: str) -> None:
    """ remove if exist """
    if isfile(filepath):
        remove(filepath)

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

def csv_write(filepath: str, data: list[Any]):
    """
    Writes a Python list to a file in CSV format.

    This function overwrites the file if it already exists.
    """
    with open(filepath,'w',newline="") as f:
              
        w = csv.writer(f,delimiter='|',)
        w.writerows(data)

def csv_read(filepath: str) -> list[str]:
    """Reads JSON data from a file and parses it into a Python list."""
    with open(filepath,'r',newline="") as f: 
        w = csv.reader(f,delimiter='|',)
        return [row for row in w]

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
    """
    Creates all essential folders for further use.
    """
    cnef(AUDIO_FOLDER)
    cnef(FIXED_AUDIO_FOLDER)
    cnef(THUMBNAIL_FOLDER)
    cnef(VIDEO_FOLDER)
    cnef(TAD_FOLDER)
    cnef(TEMP_FOLDER)
    cnef(BACKUP_FOLDER)
    cnef(DEPLOY_FOLDER)
    cnef(AC_RESULT_FOLDER)
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
    """
    The lets plays table
    
    .. id::
        The index of the lp - primary key
    .. tad_path::
        This is used to get the TAD file stored in ´{TAD_PATH}/{filename}´
    .. name::
        the lets plays name.
        USE ONLY: `a - z` & ´_´ otherwise the app can crash. See issue #236
    .. game_name::
        the game_name
        this can be the name of your series
    .. episode_length::
        is used to inform the user about reaching the recording time limit. See issue #204
    .. description_path::
        This is used to get the full description for a specific lp
    """
    __tablename__ = 'letsplays'
    id = Column(Integer, primary_key=True)
    tad_path = Column(String)
    name = Column(String)
    game_name = Column(String)
    episode_length = Column(Integer)
    description_path = Column(String)

class Episodes(Base):
    """
    The episodes table
    
    **WARNING**: 
        This table stores ALL episodes from ALL lets plays you working with!
    
    .. id::
        The index of the ep - primary key
    .. lpid::
        the index of the linked lp
    .. video_path::
        the recording path from OBS
    .. audio_mic_path::
        This is used to easy access the fetched audio from episodes
    .. audio_desktop_path::
        This is used to easy access the fetched audio from episodes
    .. thumbnail_path::
        This is used to easy access the generated thumbnail from episodes
    .. has_problem::
        NOT IN USE! Functionality will be added in later versions, see issue #238
        Indicates that the user has to do some work manually.
    .. audio_mic_edit1_path::
        WILL BE REMOVED later. See issue #239
        This is used to easy access the fixed audio from episodes
    .. audio_mic_edit2_path::
        WILL BE REMOVED later. See issue #239
        This is used to easy access the audacity fixed audio from episodes
    .. title::
        This will be used in deploy for easy upload.
    .. upload_at::
        NOT IN USE! See issue #241
        This will be used in deploy for easy upload.
    .. final_video_path::
        This will used in deploy for easy upload.
    """
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True)
    lpid = Column(Integer,default=0)
    video_path = Column(String)
    audio_mic_path = Column(String)
    audio_desktop_path = Column(String)
    thumbnail_path = Column(String)
    has_problem = Column(Integer)
    audio_mic_edit1_path = Column(String)
    audio_mic_edit2_path = Column(String)
    title = Column(String)
    upload_at = Column(String)
    final_video_path = Column(String)

class SQLAccess:
    """
    A Wrapper Class for all Lets Play & Episode Data Handling.
    ---
    """
    
    def create_from_csv():
        """
        Initializes and populates the database with data from CSV files.

        This function orchestrates the import of both 'letsplays' and 'episodes'
        data. It first ensures a clean state by closing any existing database
        connections, backing up the current database file, and removing it. A new,
        fresh database and session are then created.

        It reads data from `lets_play_export.csv` and `episodes_export.csv`,
        iteratively adding the records to the respective tables using the
        `SQLAccess` wrapper class. The function commits the changes to the database
        and properly closes the session and disposes of the engine at the end.
        """
        
        if not isfile('lets_play_export.csv') or not isfile('episodes_export.csv'): 
            xerr('You have no exported files') # TODO - Translation needed
            return
        
        SQLAccess.close_and_dispose()
        SQLAccess.backup_and_remove()
        
        session, engine, _ = SQLAccess.connect()

        data = csv_read('lets_play_export.csv')
        SQLAccess.import_lets_plays(session,data)
        
        data = csv_read('episodes_export.csv')
        SQLAccess.import_episodes(session, data)
        
        session.commit()
        SQLAccess.close_and_dispose(session, engine)
    
    def connect():
        engine = create_engine(DB_URL)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session, engine, Session
    
    def close_and_dispose(s=None,e=None):
        if s is None:
            session.close()
        else:
            s.close()
        if e is None:
            engine.dispose()
        else:
            e.dispose()

    def backup_and_remove():
        copyfile(DB_PATH, f"{DB_PATH.split('.')[0]}{dt.now().strftime('%y_%m_%d_%H_%M_%S_')}_backup_{DB_PATH.split('.')[1]}x")
        remove(DB_PATH)
    
    def export_lpep():
        csv_write('episodes_export.csv', SQLAccess.get_episodes_as_list())
        csv_write('lets_play_export.csv', SQLAccess.get_lets_plays_at_list())
    
    def import_lets_plays(session, data: list):
        for description_path, episode_length, game_name, id, name, tad_path in data:
            lp = LetsPlays(
                description_path = description_path,
                episode_length = episode_length,
                game_name = game_name,
                id = id,
                name = name,
                tad_path = tad_path
            )
            session.add(lp)
    
    def import_episodes(session, data: list):
        for idx, (_, id, lpid, thumbnail_path, video_path, audio_mic_path, audio_desktop_path, audio_mic_edit1_path, audio_mic_edit2_path, final_video_path, has_problem, title, upload_at) in enumerate(data, 0):
            ep = Episodes(
                id = idx,
                lpid = lpid,
                thumbnail_path = thumbnail_path,
                video_path = video_path,
                audio_mic_path = audio_mic_path,
                audio_desktop_path = audio_desktop_path,
                audio_mic_edit1_path = audio_mic_edit1_path,
                audio_mic_edit2_path = audio_mic_edit2_path,
                final_video_path = final_video_path,
                has_problem = has_problem,
                title = title,
                upload_at = upload_at
            )
            session.add(ep)
    
    def get_episodes_as_list() -> list:
        _ret = []
        for ep in SQLAccess.read_all_episodes():
            ep: Episodes
            _ret.append([
                SQLAccess.read_letsplay_name(SQLAccess.read_letsplay_ids().index(ep.lpid)),
                ep.id,
                ep.lpid,
                ep.thumbnail_path,
                ep.video_path,
                ep.audio_mic_path,
                ep.audio_desktop_path,
                ep.audio_mic_edit1_path,
                ep.audio_mic_edit2_path,
                ep.final_video_path,
                ep.has_problem,
                ep.title,
                ep.upload_at,
            ])
        return _ret
    
    def get_lets_plays_at_list() -> list:
        _ret = []
        for lp in SQLAccess.read_letsplays():
            lp: LetsPlays
            _ret.append([lp.description_path,
            lp.episode_length,
            lp.game_name,
            lp.id,
            lp.name,
            lp.tad_path])
        return _ret
            
    
    def get_ep_by_id(lpid: int):
        """
        Retrieves the ID of a specific episode from a letsplay.
        
        Args:
            lpid (int): The index of the letsplay to retrieve the episode from.

        Returns:
            int: The ID of the episode.
        """
        return SQLAccess.read_episodes()[lpid].lpid

    def __cvtid(lpid) -> int:
        """
        Converts a letsplay index to its database ID.
        
        Args:
            lpid (int): The index of the letsplay.
            
        Returns:
            int: The database ID of the letsplay.
        """
        return SQLAccess.read_letsplays()[lpid].id

    def create_episode(lpid: int, video_path: str):
        """
        Creates a new episode entry in the database.
        
        Args:
            lpid (int): The index of the letsplay the episode belongs to.
            video_path (str): The file path to the video for the episode.
        """
        data = Episodes(video_path=video_path, lpid=SQLAccess.__cvtid(lpid))
        session.add(data)
        session.commit()
        
    def create_letsplay(name: str, game_name: str, episode_length: int):
        """
        Creates a new letsplay entry in the database.
        
        Args:
            name (str): The name of the letsplay.
            game_name (str): The name of the game in the letsplay.
            episode_length (int): The planned length of each episode in minutes.
        """
        data = LetsPlays(name=name, game_name=game_name, episode_length=episode_length)
        session.add(data)
        session.commit()

    def read_letsplays() -> list[LetsPlays]:
        """
        Reads all letsplay entries from the database.
        
        Returns:
            list[LetsPlays]: A list of all letsplay objects.
        """
        return [letsplay for letsplay in session.query(LetsPlays).all()]
    
    def read_all_episodes() -> list[Episodes]:
        """
        Reads all episode entries from the database.
        
        Returns:
            list[Episodes]: A list of all episode objects.
        """
        return [episodes for episodes in session.query(Episodes).all()]

    def read_episodes(lpid: int) -> list[Episodes]:
        """
        Reads all episodes belonging to a specific letsplay.
        
        Args:
            lpid (int): The index of the letsplay.
        
        Returns:
            list[Episodes]: A list of episode objects for the specified letsplay.
        """
        return [episodes for episodes in session.query(Episodes).all() if episodes.lpid == SQLAccess.__cvtid(lpid)]

    def update_letsplay(lpid: int, episode_length: int):
        """
        Updates the episode length of a specific letsplay.
        
        Args:
            lpid (int): The index of the letsplay to update.
            episode_length (int): The new planned length of each episode in minutes.
        """
        data = SQLAccess.read_letsplays()
        data[lpid].episode_length = episode_length
        session.commit()

    def update_tadpath(lpid: int, tad_path: int):
        """
        Sets the 'tad_path' attribute for a specific letsplay.
        
        Args:
            lpid (int): The index of the letsplay.
            tad_path (int): The new value for 'tad_path'.
        """
        data = SQLAccess.read_letsplays()
        data[lpid].tad_path = tad_path
        session.commit()

    def update_episode(lpid: int, epid: int, **kwargs):
        """
        Updates attributes of a specific episode.
        
        Args:
            lpid (int): The index of the letsplay.
            epid (int): The index of the episode to update.
            **kwargs: Arbitrary keyword arguments representing attribute names and their new values.
        """
        data = SQLAccess.read_episodes(lpid)[epid]
        for key in kwargs:
            if not hasattr(data, key):
                raise NameError(f'The attribute: [{key}] does not exist!')
            data.__setattr__(key, kwargs[key])
        session.commit()

    def clear_and_renew_db(data: list[list]) -> bool:
        session.close() # close the database(global)
        
        DB_PATH = f'{ROOT}lprt.db'
        copyfile(DB_PATH, DB_PATH + 'x') # <- create the backup. lprt.dbx
        remove(DB_PATH) # <- remove the original db
        #Create the db again
        Base = declarative_base()
        engine = create_engine(DB_URL)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        #TODO Create all lets plays
        #TODO Create all episodes
        
        sys.exit() # after finishing, close app
    
    def delete_letsplay(lpid: int):
        """
        Deletes a letsplay and all its associated episodes.
        
        Args:
            lpid (int): The index of the letsplay to delete.
        """
        data = session.query(LetsPlays).all()[lpid]
        session.delete(data)
        while SQLAccess.read_episodes(lpid):
            SQLAccess.delete_episode(lpid, 0)
        session.commit()

    def delete_episode(lpid: int, epid: int):
        """
        Deletes a specific episode from the database.
        
        Args:
            lpid (int): The index of the letsplay the episode belongs to.
            epid (int): The index of the episode to delete.
        """
        data = session.query(Episodes).filter(SQLAccess.__cvtid(lpid) == Episodes.lpid).all()[epid]
        session.delete(data)
        session.commit()
            
    def read_letsplay_names():
        """
        Retrieves all letsplay names from the database.
        
        Returns:
            list: A list of letsplay names.
        """
        return [entry.name for entry in session.query(LetsPlays).all()]

    def read_episode_length(lpid: int):
        """
        Retrieves the 'episode_length' for a specific letsplay.
        
        Args:
            lpid (int): The index of the letsplay.
        
        Returns:
            str: The 'episode_length' for the letsplay.
        """
        return [entry.episode_length for entry in session.query(LetsPlays).all()][lpid]

    def read_tad_path(lpid: int):
        """
        Retrieves the 'tad_path' for a specific letsplay.
        
        Args:
            lpid (int): The index of the letsplay.
        
        Returns:
            str: The 'tad_path' for the letsplay.
        """
        return [entry.tad_path for entry in session.query(LetsPlays).all()][lpid]

    def read_letsplay_name(lpid: int):
        """
        Retrieves the name of a specific letsplay.
        
        Args:
            lpid (int): The index of the letsplay.
        
        Returns:
            str: The name of the letsplay.
        """
        return [entry.name for entry in session.query(LetsPlays).all()][lpid]

    def read_letsplay_game_name(lpid: int):
        """
        Retrieves the game name of a specific letsplay.
        
        Args:
            lpid (int): The index of the letsplay.
        
        Returns:
            str: The game name of the letsplay.
        """
        return [entry.game_name for entry in session.query(LetsPlays).all()][lpid]

    def read_letsplay_description(lpid: int):
        """
        Retrieves the description path of a specific letsplay.
        
        Args:
            lpid (int): The index of the letsplay.
        
        Returns:
            str: The description path of the letsplay.
        """
        return [entry.description_path for entry in session.query(LetsPlays).all()][lpid]

    def read_letsplay_game_names():
        """
        Retrieves all game names from the database.
        
        Returns:
            list: A list of game names from all letsplays.
        """
        return [entry.game_name for entry in session.query(LetsPlays).all()]

    def read_letsplay_ids():
        """
        Retrieves all letsplay IDs from the database.
        
        Returns:
            list: A list of letsplay IDs.
        """
        return [entry.id for entry in session.query(LetsPlays).all()]

    def read_video_path(lpid: int, epid: int):
        """
        Retrieves the video path for a specific episode.
        
        Args:
            lpid (int): The index of the letsplay.
            epid (int): The index of the episode.
            
        Returns:
            str: The video path for the episode.
        """
        return [entry.video_path for entry in session.query(Episodes).all() if entry.lpid == SQLAccess.__cvtid(lpid)][epid]

    def read_title(lpid: int, epid: int):
        """
        Retrieves the title of a specific episode.
        
        Args:
            lpid (int): The index of the letsplay.
            epid (int): The index of the episode.
        
        Returns:
            str: The title of the episode.
        """
        return [entry.title for entry in session.query(Episodes).all() if entry.lpid == SQLAccess.__cvtid(lpid)][epid]

    def read_thumbnail_path(lpid: int, epid: int):
        """
        Retrieves the thumbnail path for a specific episode.
        
        Args:
            lpid (int): The index of the letsplay.
            epid (int): The index of the episode.
        
        Returns:
            str: The thumbnail path for the episode.
        """
        return [entry.thumbnail_path for entry in session.query(Episodes).all() if entry.lpid == SQLAccess.__cvtid(lpid)][epid]

    def read_final_video_path(lpid: int, epid: int):
        """
        Retrieves the final video path for a specific episode.
        
        Args:
            lpid (int): The index of the letsplay.
            epid (int): The index of the episode.
        
        Returns:
            str: The final video path for the episode.
        """
        return [entry.final_video_path for entry in session.query(Episodes).all() if entry.lpid == SQLAccess.__cvtid(lpid)][epid]

    def read_episode_ammount(lpid: int):
        """
        Retrieves the total number of episodes for a specific letsplay.
        
        Args:
            lpid (int): The index of the letsplay.
        
        Returns:
            int: The number of episodes.
        """
        return len([entry for entry in session.query(Episodes).all() if entry.lpid == SQLAccess.__cvtid(lpid)])

    def read_letsplay_by_option_var(parent):
        """
        Converts the lp_option_var index to database index.
        
        Args:
            parent: An object containing a `lp_option_var` attribute.
        
        Returns:
            int: The index of the letsplay name.
        """
        return SQLAccess.read_letsplay_names().index(parent.lpep_picker.v_lp.get())


session, engine, Session = SQLAccess.connect()
