from bin.workflow_modules import *
from yaml import safe_load
from bin.constants import (
    FIXED_AUDIO_FOLDER
)

DEFAULT_CONTEXT = {
    'FIXED_AUDIO_FOLDER': FIXED_AUDIO_FOLDER
}

WHITELIST_MODULES = {
    'data_access': DataAccess,
    'ffmpeg_api': FFMPEG_API,
    'constants': CONSTANTS,
    'ui_manager': UI_MANAGER,
    'core_helpers': CORE_HELPERS
}

class WorkflowExecutor:
    
    def __init__(self, config_data: dict, initial_context: dict):
        self.config = config_data
        self.context = initial_context.copy()
        
        self.loaded_modules = self._load_modules(config_data.get('include', ''))

    def _load_modules(self, module_list_str: str) -> dict:
        """ Checks & Loads: Modules in white-list from the include block """
        loaded = {}
        modules = [m.strip() for m in module_list_str.split('\n') if m.strip()]

        for mod_name in modules:
            if mod_name in WHITELIST_MODULES:
                loaded[mod_name] = WHITELIST_MODULES[mod_name]
                print(f"[INIT] Loaded module: '{mod_name}' successfully")
            else:
                raise ImportError(f"Modul '{mod_name}' is not in white-list or not exists")
        return loaded

    def _resolve_value(self, arg_value):
        """ Resolve $Variables from context"""
        if isinstance(arg_value, str) and arg_value.startswith('$'):
            var_name = arg_value[1:]
            if var_name in self.context:
                return self.context[var_name]
            raise NameError(f"Variable '{var_name}' nicht im Kontext gefunden.")
        
        return arg_value

    def execute_workflow(self,
                         config: dict,
                         initial_depth: int = 0):
        """Führt die Schritte im Workflow aus."""
        
        is_loop = config.get('workflow', None)
        
        if is_loop:
            config = config['workflow']
        
        RETURN_CODE = 0
        
        #print(f"\n=== Start Workflow: {self.config['name']} ===")
        
        try:
            for idx, step in enumerate(config['steps']):
                if 'call' in step:
                    call_path = step['call']
                    if '.' not in call_path:
                        raise ValueError(f"Invalid call: {call_path}. Must be 'module.function'.")
                    
                    module_name, func_name = call_path.split('.', 1)

                    if module_name not in self.loaded_modules:
                        raise PermissionError(f"Module '{module_name}' cannot be loaded, no permission")
                    
                    module = self.loaded_modules[module_name]
                    
                    if not hasattr(module, func_name):
                        raise AttributeError(f"Function '{func_name}' not found in module '{module_name}'.")
                    
                    function_to_call = getattr(module, func_name)
                    
                    args_list = [self._resolve_value(arg) for arg in step.get('args', [])]
                    
                    result = function_to_call(*args_list)
                    
                    if 'output' in step:
                        self.context[step['output']] = result
                        
                if 'loop' in step:
                    rng = [self._resolve_value(arg) for arg in step.get('range', [0,0])]
                    
                    #! ADD ENUM FUNCTIONALITY
                    self.context[step['enum']]
                    
                    for ci,i in enumerate(range(*rng)):
                        self.context[step['as']] = i
                        if 'enum' in self.context:
                            self.context[step['enum']] = ci
                        if not self.execute_workflow(step,initial_depth + 2):
                            raise Exception
        except KeyError as e:
            print(f'❌ Cannot resolve: {e} - {idx}')
            RETURN_CODE = 1
            return None
        except Exception as e:
            print(f"\n❌ FATAL ERROR in Workflow: {e} - {idx}")
            return None
            RETURN_CODE = 2
        if not initial_depth:
            print(f"\n=== Workflow ended with exit code: {RETURN_CODE} ===")
        return self.context

class UI:
    def __init__(self, parent, elements: list):
        self.menu = parent.master
        self.thread = None
        self.automation_callback = None
        self.progress_label = ttk.Label(self,)
        self.progress_label.grid(sticky='SE',row = 0, column = 2)
        
        
        for element in elements:
            name = element['name']
            id = element['id']
            master = element.get('master',None)
            if master == 'root':
                master = parent
            else:
                master = getattr(self,master[1:])
            
            if 'pack' in element:
                put_mode = 'pack'
                fill = element['pack'].get('fill',None)
                padx = element['pack'].get('padx',None)
                pady = element['pack'].get('pady',None)
                
            elif 'grid' in element: #! Not used currently
                put_options = element['grid'] 
                put_mode = 'grid'
            
            print(element['name'])
            setattr(self, element['id'])

def run_workflow(config_raw: str, initial_vars: dict):
    try:
        config_data = safe_load(config_raw)

        executor = WorkflowExecutor(config_data, initial_vars | DEFAULT_CONTEXT)
        final_context = executor.execute_workflow(executor.config)
        
        print("\n--- Summary ---")
        print("Initial Context:", initial_vars)
        print("Final Context:", final_context)
        
    except Exception as e:
        print(f"\n❌ ProgramError: {e}")
