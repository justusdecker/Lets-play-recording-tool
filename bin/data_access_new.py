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
   
        
SQPT = 'bin/data/sql/'
class Querys:
    CREATE_DB = """
    CREATE TABLE IF NOT EXISTS letsplays (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        version TEXT NOT NULL,
        tad_path TEXT NOT NULL,
        name TEXT UNIQUE NOT NULL,
        game_name TEXT UNIQUE NOT NULL,
        episode_length INTEGER NOT NULL,
        description_path TEXT NOT NULL
    )
    """
    READ_LP = """
    SELECT * FROM letsplays
    """
    CREATE_EP = """
    CREATE TABLE :name (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_path TEXT NOT NULL,
        audio_mic__path TEXT NOT NULL,
        audio_desktop_path TEXT NOT NULL,
        thumbnail_path TEXT NOT NULL,
        has_problem TEXT NOT NULL,
    )
    """
    CREATE_LP = """
    INSERT INTO letsplays ( :version , "" , :name , :game_name , :episode_length , "" )
    """

class Sql:
    """
    |id|key|
    |---|---|
    |0|id <- unused|
    |1|version|
    |2|tad|
    |3|name|
    |4|game_name|
    |5|episode_length|
    |6|description|
    """
    engine = create_engine(DB_URL, echo=True) # Create the engine echo prints the sql querys
    filepath = f'{ROOT}/data.db'
    
    def connect_exec_and_comm(self,query: str,params: dict[str,int | float | str] | None = None):
        try:
            with self.engine.connect() as connection:
                connection.execute(text(query),params)
                connection.commit()
            return True
        except Exception as E:
            print(E)
            return None
            
    def connect_exec_and_retr(self,query: str,params: dict[str,int | float | str] | None = None):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query),params)
                movies = result.fetchall()

            return [row for row in movies]
        except Exception as E:
            print(E)
            return None
    
    # Episodes
    
    def get_episodes(self,lpid: int) -> list:
        pass
    
    # Lets Plays
    
    def get_letsplays(self) -> list:
        return self.connect_exec_and_retr(Querys.READ_LP)
    
    def get_name(self,id: int):
        return self.get_letsplays()[id][3]
    def get_gamename(self,id: int):
        return self.get_letsplays()[id][4]
    def get_version(self,id: int):
        return self.get_letsplays()[id][1]
    def get_tad_path(self,id: int):
        return self.get_letsplays()[id][2]
    def get_episode_length(self,id: int):
        return self.get_letsplays()[id][5]
    def get_description_path(self,id: int):
        return self.get_letsplays()[id][6]
        
    def set_tad_path(self):
        pass
    def set_episode_length(self):
        pass
    def set_description_path(self):
        pass
    
    def create_letsplay_entry(self):
        pass
    def delete_letsplay_entry(self):
        pass    

SQL = Sql()
SQL.connect_exec_and_comm(Querys.CREATE_DB)
SQL.get_letsplays()