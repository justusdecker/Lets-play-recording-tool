import ast

with open('./bin/auto/wf_upload_at_set.py') as f:
    data = f.read()

def err(text: str) -> str:
    return f'\033[31m{text}\033[0m'

class SCOPES:
    READ = False
    WRITE = False
    RW = False
    DEL = False
    SQL_READ = False
    SQL_WRITE = False
    SQL_RW = False
    CMD_START = False
    CMD_COPY = False
    CMD_TK = False
    CMD_ATTR = False
    CMD_FFMPEG = False
    CMD_SOX = False
    ADMIN = False

class Visitor(ast.NodeVisitor):
    def visit_Del(self, node):
        return super().visit_Del(node)
    def visit_Global(self, node):
        return super().visit_Global(node)

    def visit_Import(self, node):
        
        
        print(err(f'ImportDeniedError in Line: {node.lineno} - {node.names}'))
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        print(err(f'ImportDeniedError in Line: {node.lineno} - from {node.module} import {node.names[0].name}'))
        self.generic_visit(node)
        
    def visit_Call(self, node):
        print(f'Call: {node.func}')
        self.generic_visit(node)

tree = Visitor().visit(ast.parse(data))

call_nodes = [
    node for node in ast.walk(ast.parse(data)) if isinstance(node, ast.Call)
]
print(ast.dump(ast.parse(data)))
from json import dumps
for n in call_nodes:
    print(ast.dump(n.func,indent=4))
