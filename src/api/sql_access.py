def parse_to_csv(): ...
def parse_to_json(): ...
def backup(): ...
def close_and_dispose(): ...
def connect(): ...
def backup_and_remove(): ...
from typing import Literal
from src.api.module_loader import DatabaseLoader
from src.api.constants import ROOT

from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



class SQLAccess:
    
    def __init__(self):
        self.base = declarative_base()
        config_success = self.__create_table_cfg(DatabaseLoader().ctx)
        if not config_success:
            raise NotImplementedError
        self.__connect()  
    
    def __create_table_cfg(self, ctx: str) -> bool:
        try:
            exec(ctx, globals={
                'Base': self.base
            })
            return True
        except Exception as E:
            print(E)  
        
        return False
    
    def __connect(self):
        DB_URL = f"sqlite:///{ROOT}lprt_data.db"
        
        self.engine = create_engine(DB_URL)
        self.base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
    
    def __close(self):
        ...
            
SQLA = SQLAccess()