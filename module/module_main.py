"""
LabelFrame:
    parent: self.mF
    text: Recording
    pm: PACK
    None
        
"""

from src.api import DisableWidgets, View, TkinterWidgetBuilder, ttk, tk, TK_GRID, TK_PACK
            
        
class Recording(View):
    NAME = 'Recording'
    def __init__(self, parent):
        super().__init__(parent)
        self.thread = None
        
        _LF_recording = TkinterWidgetBuilder(
            ttk.LabelFrame,
            {'master': self.mF, 'text': 'Recording'},
            TK_PACK,
            None
        )
        
        _LF_information = TkinterWidgetBuilder(
            ttk.LabelFrame,
            {'master': self.mF, 'text': 'Information'},
            TK_PACK,
            None
        )
        
        self.BTN_connect = TkinterWidgetBuilder(
            ttk.Button,
            {'master': _LF_recording, 'text': 'Connect', 'command': self.get_connection},
            TK_PACK,
            {'side':tk.BOTTOM}
        )
        
        self.LPEP = None #! Missing LPEP Template!
        
        self.L_recording_info = TkinterWidgetBuilder(
            ttk.Label,
            {'master': _LF_information, 'text': 'No connection'},
            TK_GRID,
            {'row': 0, 'column': 1}
        )

    def get_connection(self): ...
    def __get_connection(self): ...
    def __on_lp_change(self): 
        DisableWidgets(self.BTN_connect)
    def update_recording_information(self, text: str): ...
    def obs_connection(self): ...
    
class FetchAudio(View):
    NAME = 'FetchAudio'
    def __init__(self, parent):
        super().__init__(parent)
        
        _LF_recording = TkinterWidgetBuilder(
            ttk.LabelFrame,
            {'master': self.mF, 'text': 'Recording'},
            TK_PACK,
            None
        )
        self.BTN_connect = TkinterWidgetBuilder(
            ttk.Button,
            {'master': _LF_recording, 'text': 'Connect', 'command': self.get_connection},
            TK_PACK,
            {'side':tk.BOTTOM}
        )
        
        

    def get_connection(self): ...
    def __get_connection(self): ...
    def __on_lp_change(self): ...
    def update_recording_information(self, text: str): ...
    def obs_connection(self): ...