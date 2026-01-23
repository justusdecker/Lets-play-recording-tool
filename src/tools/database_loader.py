from api.sql_access import SQLA


PATH: str = './module/'

class DatabaseLoader:
    def __init__(self):
        self.ctx = ''
        self.__acr = ''
        self.__create_database_from_template()
        self.__write()
    
    def __write(self):
        with open(f'{PATH}db.py', 'w') as file:
            file.write(self.ctx)
    
    def __add_context(self, ctx: str):
        self.ctx += ctx + '\n'
        
    def __add_context_acr(self, ctx: str):
        self.__acr += ctx + '\n'
    
    def __create_column(self, data: str):
        name, values = data.split(':')
        
        if '->' in data:
            types, default = values.split('->')
            has_default = True
        else:
            has_default = False
            types, default = values, None
        
        if ',' in types:
            type, primary = types.split(',')
        else:
            type, primary = types, None
        
        name = name.strip()
        type = type.strip()
        
        if type == 'Text':
            type = 'String'
        
        primary = primary.strip() if primary is not None else primary
        default = default.strip() if default is not None else default
        
        self.__add_context(f"    {name} = Column({type}{', primary_key=True' if primary else ''}{f', default={default}' if has_default else ''})")
    
    def __create_endpoints_for_each_method(self,tablename: str):
        """
        creates a sql-access structure like:
        
        class ACCESSOR:
            def <table>_read(<key or id>)
            def <table>_update(<key or id>, **data) <- raises an error if data is not valid!
            def <table>_delete(<key or id>) <- raises an error if not exist
            def <table>_safe_delete(<key or id>) <- checks for missing entry
            def <table>_create(<key or id>, **data) <- raises an error if not nullable values are none!
            def <table>_clear()
            """
        # TODO: Implement the CRUD Methods as raw strings and copy them at the end of self.ctx
        read_str = f"    def {tablename}_read(id_or_key: int | str):\n"
        SQLA.session.query()
    
        self.__add_context_acr(f"    def {tablename}_read")

    def __create_database_from_template(self):
        self.__add_context('from sqlalchemy import Column, Integer, String, Numeric, Boolean')
        self.__add_context('from src.api.sql_access import SQLA')
        self.__add_context_acr('class ACCESSOR:')
        with open(f'{PATH}base.sql') as file:
            template = file.read()
        
        lines = template.splitlines()
        for idx, line in enumerate(lines):
            if line.startswith('<Table'):
                tablename = line.replace('<Table@\'', '')[:-2]
                self.__create_endpoints_for_each_method(tablename)
                self.__add_context(f'class {tablename}(SQLA.base):')
                self.__add_context(f'    __tablename__ = \'{tablename}\'')
                for selected_line in lines[idx+1:]:
                    if not selected_line.startswith(' ' * 4):
                        break
                    self.__create_column(selected_line)
                
if __name__ == '__main__':
    DatabaseLoader()