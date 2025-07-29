from sqlalchemy import create_engine, text

from bin.constants import ROOT

DB_URL = "sqlite:///movies.db" # Define the database URL

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
        
SQL_CRT_LP = file_read('bin/sql/crt_letsplays.sql')

class SQL:
    engine = create_engine(DB_URL, echo=True) # Create the engine echo prints the sql querys
    filepath = f'{ROOT}/data.db'
    def create_letsplays(self):
        with self.engine.connect() as connection:
            connection.execute(text(SQL_CRT_LP))
            connection.commit()
    
    def connect_and_commit(self,query: str,params: dict[str,int | float | str]):
        try:
            with self.engine.connect() as connection:
                connection.execute(text(query,params))
                connection.commit()
            return True
        except Exception as E:
            print(E)
            return None
            
    def connect_and_retreive(self):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
                movies = result.fetchall()

            return [row for row in movies]
        except:
            return None
    
    def get_episodes(self,lpid: int) -> list:
        pass
    
    
    
    def get_letsplays(self) -> list:
        pass
    
    