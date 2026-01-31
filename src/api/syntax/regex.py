from typing import Callable, Iterator
from jinja2 import Template
def render_template(text: str, **replacers):
    return Template(text).render(**replacers)
from re import Match, search, finditer, MULTILINE


GET_CLASS_NAME_AND_CONTEXT = r'^@(\w+):((?:\n(?:[ \t].*|$))*)'
GET_FUNCTION_NAME_AND_CONTEXT = r'^[ ]{4}\.(\w+):([\s\S]*?)(?=^[ ]{4}\.|\Z)'

GET_LINE_OR_COMMENT = r'^\s{8}((\/\/.*)|(.*))'
GET_PYTHON_LINES = r'>((\n|.)*?)<'

SPLIT_LINE = r'([\w_]+)\s?=\s?(.*)'
GET_NORMAL_VARIABLE = r'^(None|True|False|[+-]?[0-9]\.?[0-9]?|\'[^\']*\'|\"[^\"]*\")$'
GET_INSTANCIATON = r'^(\w+)\((.*)\)'
GET_FUNCTION_CALL = r'^\w+\(.*\)'
GET_INSTANCION_VARIABLES = r''

TEMPLATE_TK = """
            self.{{var_name}} = {{uie}}({{parent}}, text={{text}})
            self.{{var_name}}.{{pack_method}}({{pm_args}})
"""[1:-1]

TEMPLATE_FUNC_CALL_DISABE_ENABLE = """
            {{function}}(self.{{object}})
"""[1:-1]


TEST = """
@Recording:
    .View:
        thread = None
        RECORDING = LFrame(mF, "Recording", Pack) 
        // wird zu self.RECORDING = ttk.LabelFrame(self.mainframe,"Recording")
        // self.RECORDING.pack()
        INFORMATION = LFrame(mF, "Information")
        connect_btn = Btn(RECORDING, "Connect to OBS", get_connection)
        Pack(connect_btn, 'bottom')
        LPEP = LPEPPicker(RECORDING, run_callback, "lp-nb", lp_changed)
        RECORDING_TIME_LABEL = Label(mF, "No Connection", Grid, {r:0, c:1, px:10, py:10})
        AutoPack() // Packs all UI Elements automatically, if not specified or already set!
        Disable(connect_btn)
    .Automation:
        ...
    .Custom:
        > 
        def lp_changed(self,*args):
            Enable(self.connect_btn)

        def get_connection(self):
            if self.thread:
                self.close_connection = True
            Disable(self.LPEP)
            if self.thread is None:
                self.close_connection = False
                self.thread = Thread(target=self.__get_connection)
                self.thread.start()
        def __get_connection(self):
            Disable(self.menu) # Deactivates all menu buttons for safety reasons
            Disable(self.btn_connect)
            self.btn_connect.configure(text=gtran("bin::ui::recording::connect_btn_text_try_connecting"))
            obs_connect(self)
            Enable(self.btn_connect)
            Enable(self.menu) # Reactivating
            if not self.close_connection:
                self.btn_connect.configure(text=gtran("bin::ui::recording::connect_btn_text_error_occured"))
            self.thread = None
            change_states(self.lpep_picker.get_ui(),'!disabled')
        <
@Recording:
    .View:
        thread = None
        RECORDING = LFrame(mF, "Recording", Pack) 
        // wird zu self.RECORDING = ttk.LabelFrame(self.mainframe,"Recording")
        // self.RECORDING.pack()
        INFORMATION = LFrame(mF, "Information")
        connect_btn = Btn(RECORDING, "Connect to OBS", get_connection)
        Pack(connect_btn, 'bottom')
        LPEP = LPEPPicker(RECORDING, run_callback, "lp-nb", lp_changed)
        RECORDING_TIME_LABEL = Label(mF, "No Connection", Grid, {r:0, c:1, px:10, py:10})
        AutoPack() // Packs all UI Elements automatically, if not specified or already set!
        Disable(connect_btn)
    .Automation:
        ...
    .Custom:
        > 
        def lp_changed(self,*args):
            Enable(self.connect_btn)

        def get_connection(self):
            if self.thread:
                self.close_connection = True
            Disable(self.LPEP)
            if self.thread is None:
                self.close_connection = False
                self.thread = Thread(target=self.__get_connection)
                self.thread.start()
        def __get_connection(self):
            Disable(self.menu) # Deactivates all menu buttons for safety reasons
            Disable(self.btn_connect)
            self.btn_connect.configure(text=gtran("bin::ui::recording::connect_btn_text_try_connecting"))
            obs_connect(self)
            Enable(self.btn_connect)
            Enable(self.menu) # Reactivating
            if not self.close_connection:
                self.btn_connect.configure(text=gtran("bin::ui::recording::connect_btn_text_error_occured"))
            self.thread = None
            change_states(self.lpep_picker.get_ui(),'!disabled')
        <
"""

class ContextManager:
    def __init__(self, ctx: str, ctx_callback: Callable) -> None:
        self.ctx_callback = ctx_callback
        self.ctx = ctx
        self.result: Iterator[Match[str]] | Match[str] | None = None
        self.parse()
        self.deepify()
        #if self.result is None: raise Exception
      
class Class(ContextManager):
    REGEX = r'^@(\w+):((?:\n(?:[ \t].*|$))*)'
    
    TEMPLATE = """
class {{name}}(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.menu = parent.master
        self.mainframe = ttk.Frame(parent)
        self.mainframe.pack(expand = True, fill tk.Both)
"""[1:-1]
    
    def __init__(self, ctx: str, ctx_callable: Callable) -> None:
        super().__init__(ctx, ctx_callable)
    
    def parse(self):
        self.result = finditer(Class.REGEX, self.ctx, MULTILINE)
    
    def deepify(self):
        for result in self.result:
            _template = render_template(Class.TEMPLATE, **{'name': result.group(1)})
            self.ctx_callback(_template)
            Function(result.group(2), self.ctx_callback)
        
class Function(ContextManager):
    REGEX = r'^[ ]{4}\.(\w+):([\s\S]*?)(?=^[ ]{4}\.|\Z)'
    
    def __init__(self, ctx: str, ctx_callable: Callable) -> None:
        super().__init__(ctx, ctx_callable)
    
    def parse(self): 
        self.result = finditer(Function.REGEX, self.ctx, MULTILINE)
    
    def deepify(self): 
        # Automation bekommt eine eigene Klasse im auto/
        # View kommt ins __init__
        # Custom wird unten nach __init__ angehangen
        
        for result in self.result:
            
        
            name = result.group(1)
            content = result.group(2)
            match name:
                case 'View':
                    Lines(content, self.ctx_callback)
                case 'Automation':
                    # Hier müssen wir eine eigene Klasse erstellen, kommt später
                    ...#raise NotImplementedError
                    
                case 'Custom':
                    # Wird nach dem Init angehangen
                    # Muss zusätzlich in CustomPython geparst werden.
                    # Das Ergebnis kommt in das Resultat.
                    ...#raise NotImplementedError
    
class Lines(ContextManager):
    REGEX = r'^\s{8}((\/\/.*)|(.*))'
    REGEX2 = r'([\w_]+)\s?=\s?(.*)'
    
    def __init__(self, ctx: str, ctx_callback: Callable) -> None:
        super().__init__(ctx, ctx_callback)

    def parse(self):
        self.result = finditer(GET_LINE_OR_COMMENT, self.ctx, MULTILINE)
    
    def deepify(self): 
        for line in self.result:
            line = line.group(1)
            if line is None: continue
            
            if line.startswith('//'): continue
            line = line.strip()
            
            call = Call(line.strip(), self.ctx_callback)
            if call.is_okay: continue
            
            normal_variable = NormalVariable(line.strip(), self.ctx_callback)
            if normal_variable.is_okay: continue
            
            instance = InstanceToVariable(line.strip(), self.ctx_callback)
            if instance.is_okay: continue
     
class NormalVariable(ContextManager):
    REGEX = r'\w+\s*=\s*\w+$'
    TEMPLATE = """
        self.{{function}} = {{object}}
"""[1:-1]
    def __init__(self, ctx: str, ctx_callback: Callable) -> None:
        super().__init__(ctx, ctx_callback)
        self.is_okay = False
        
    def parse(self):
        self.result = search(NormalVariable.REGEX, self.ctx)
        self.is_okay = self.result is not None
        
    def deepify(self): 
        if self.is_okay:
            name, obj = self.result.group().split('=')
            name, obj = name.strip(), obj.strip()
            _template = render_template(NormalVariable.TEMPLATE, **{'function': name, 'object': obj})
            self.ctx_callback(_template)
    
class InstanceToVariable(ContextManager):
    REGEX = ''
    def __init__(self, ctx: str, ctx_callback: Callable) -> None:
        super().__init__(ctx, ctx_callback)
        self.is_okay = False
    
    def parse(self):
        return
        self.result = search(InstanceToVariable.REGEX, self.ctx)
        self.is_okay = self.result is not None
    
    def deepify(self): ...
    
      
class Call(ContextManager):
    REGEX = r'^\w+\(.*\)'
    
    def __init__(self, ctx: str, ctx_callback: Callable) -> None:
        super().__init__(ctx, ctx_callback)
        self.is_okay = False
        
    def parse(self):
        self.result = search(Call.REGEX, self.ctx)
        self.is_okay = self.result is not None
        
    def deepify(self): ...

    
class CallArguments:
    ...
    
class CustomPython:
    ...

class Converter:
    def __init__(self, script: str) -> None:
        self.ctx = ''
        Class(script,self.add_ctx)
        print(self.ctx)
        
    def add_ctx(self, ctx: str):
        self.ctx += ctx + '\n'

Converter(TEST)