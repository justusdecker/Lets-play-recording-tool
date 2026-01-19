from bin.views.modules import GridLayout, Button

from bin.template.builder import button_builder

class MenuBar(GridLayout):
    def __init__(self, **kwargs):
        self.app = kwargs.pop('app')
        super().__init__(**kwargs)
        
        self.cols = 1
        self.size_hint = (0.3, 1.)
        #TODO Slider!
        letsplay_c_switcher = button_builder(
            parent=self,
            on_press_callback=self.switch2letsplayview,
            
            text = 'View Lets Plays',
            bold = True,
            background_color = '33cccc',
            background_normal = '',
            size_hint = (0.2, 0.1)
        )
        
        letsplay_c_switcher = button_builder(
            parent=self,
            on_press_callback=self.switch2letsplayview,
            
            text = 'View Episodes',
            bold = True,
            background_color = '33cccc',
            background_normal = '',
            size_hint = (0.2, 0.1)
        )
        
    def switch2letsplayview(self, *_):
        self.app.screen_manager.current = 'letsplayListView'