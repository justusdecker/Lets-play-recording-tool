from sqlalchemy import create_engine, text

DB_URL = "sqlite:///movies.db" # Define the database URL

class SQL:
    engine = create_engine(DB_URL, echo=True) # Create the engine echo prints the sql querys
    
    def create_letsplays(self):
        with self.engine.connect() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS letsplays (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version TEXT UNIQUE NOT NULL,
                    tad_path TEXT UNIQUE NOT NULL,
                    name TEXT UNIQUE NOT NULL,
                    game_name TEXT UNIQUE NOT NULL,
                    episode_length INTEGER NOT NULL,
                    description_path TEXT UNIQUE NOT NULL
                )
            """))
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
            
class CSVObj:

    def __init__(self, filepath: str,KEYS: dict):
        self.filepath = filepath
        self.data = csv_read(filepath)
        for row in self.data:
            if len(row) != len(KEYS):
                raise IndexError()
    def __check_list(self,cl:list[str],**kwargs):
        if len(cl) != len(kwargs):
            raise IndexError(f'Length of a != b')
        for e in cl:
            if e not in kwargs:
                raise KeyError(f'cannot find: {e} in {kwargs}')
    
    def __check_id(self,id: int):
        if id >= len(self.data):
            raise IndexError()
        if not isinstance(id,int):
            raise TypeError()
    
    def save(self):
        csv_write(self.filepath, self.data)
    
    def create(self,checklist: list[str], **kwargs) -> None:
        self.__check_list(cl=checklist, **kwargs)
        self.data.append([kwargs[arg] for arg in kwargs])
        
    def read(self,id: int):
        self.__check_id(id)
        return self.data[id]
    
    def update(self,id: int,checklist: list[str],**kwargs):
        self.__check_list(cl=checklist, **kwargs)
        self.__check_id(id)
        self.data[id] = kwargs
        
    def delete(self,id: int):
        self.__check_id(id)
        self.data.pop(id)
        
    @property
    def row(self) -> int:
        return len(self.data)
    
    @property
    def col(self) -> int:
        if not self.data:
            return 0
        return len(self.data[0])
