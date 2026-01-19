from bin.views.modules import *
from bin.data_access import SQLAccess
from bin.template.builder import button_builder

SELECTED_LETSPLAY = [-1]

class letsplayListView(BoxLayout):
    def __init__(self, **kwargs):
        self.app = kwargs.pop('app')
        super().__init__(**kwargs)
        
        self.ptrs = []
        
        self.lp_view = ScrollView()
        self.lp_list = GridLayout(size_hint_y=None)
        self.lp_view.size_hint=(1.,1.)
        self.lp_list.cols = 4
        self.lp_list.bind(minimum_height=self.lp_list.setter('height'))
        self.lp_view.add_widget(self.lp_list)
        self.add_widget(self.lp_view)
        

        self.add_database_entry()
        
    def add_database_entry(self):
        for lp in SQLAccess.read_letsplays():
            self.add_row(lp)

    def add_row(self,data):
        row_height = 40
        print(data.name)
        
        id = Label(text=str(data.id), size_hint_x=0.1, size_hint_y=None, height=row_height)
        self.lp_list.add_widget(id)
        
        name = Label(text=data.name, size_hint_y=None, height=row_height)
        self.lp_list.add_widget(name)
        
        game_name = Label(text=str(data.game_name), size_hint_y=None, height=row_height)
        self.lp_list.add_widget(game_name)
        btn = button_builder(
            parent=self.lp_list, 
            on_press_callback=self.lookup_letsplay,
            text = 'Edit',
            bold = True,
            background_color = 'cc33cc',
            background_normal = '')

        self.ptrs.append(btn)
    
    def lookup_letsplay(self, btn):
        idx = self.ptrs.index(btn)
        SELECTED_LETSPLAY[0] = idx
        self.app.screen_manager.current = 'letsplaySingleView'
        #SQLAccess.read_letsplays()[idx]
        print(112)
        
class letsplaySingleView(BoxLayout):
    def __init__(self, **kwargs):
        self.app = kwargs.pop('app')
        super().__init__(**kwargs)
        
        self.lp_view = ScrollView()
        self.lp_list = GridLayout(size_hint_y=None)
        self.lp_list.cols = 1
        self.lp_view.size_hint=(0.7,1.)
        
        self.lp_list.bind(minimum_height=self.lp_list.setter('height'))
        self.lp_view.add_widget(self.lp_list)
        self.add_widget(self.lp_view)
    
    def update_letsplay(self, idx: int): #? Wie update
        ...