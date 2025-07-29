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
    
engine = create_engine(DB_URL, echo=True) # Create the engine echo prints the sql querys

# create the users table
Base.metadata.create_all(engine)

# create a session to manage the connection to the database
Session = sessionmaker(bind=engine)
session = Session()

# Create Values
eps = Episodes(video_path='123.mp4')
session.add(eps)
session.commit()

# Read Values
for episode in session.query(Episodes).all():
    print(episode.video_path, episode.id)


# Update Values
for episode in session.query(Episodes).all():
    episode.video_path = 'test'
    print(episode.video_path, episode.id)
session.commit()

# Delete Values
byebye = session.query(Episodes).all()[0]
session.delete(byebye)
session.commit()