from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bin.constants import ROOT

DB_URL = f"sqlite:///{ROOT}lprt_data.db" # Define the database URL

Base = declarative_base()

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
    
    def create_episode(lpid: int, video_path: str):
        data = Episodes(video_path=video_path, lpid=SQLAccess.read_letsplays()[lpid].id)
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
        return [episodes for episodes in session.query(Episodes).all() if episodes.lpid == SQLAccess.read_letsplays()[lpid].id]
    
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
        id = SQLAccess.read_letsplays()[lpid].id
        print(f'id:{id}')
        data = session.query(Episodes).filter(id == Episodes.lpid).all()[epid]
        session.delete(data)
        session.commit()