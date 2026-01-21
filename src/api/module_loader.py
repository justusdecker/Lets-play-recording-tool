PATH: str = './module/'

class DatabaseLoader:
    def __init__(self):
        self.ctx = ''
        self.__create_database_from_template()
    
    def __add_context(self, ctx: str):
        self.ctx += ctx + '\n'
    
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
        
    def __create_database_from_template(self):
        with open(f'{PATH}base.sql') as file:
            template = file.read()
        
        lines = template.splitlines()
        for idx, line in enumerate(lines):
            if line.startswith('<Table'):
                tablename = line.replace('<Table@\'', '')[:-2]
                self.__add_context(f'class {tablename}(Base):')
                self.__add_context(f'    __tablename__ = \'{tablename}\'')
                for selected_line in lines[idx+1:]:
                    if not selected_line.startswith(' ' * 4):
                        break
                    self.__create_column(selected_line)
                    
                    
