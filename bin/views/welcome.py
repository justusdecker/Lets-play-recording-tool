from bin.views.modules import *
from bin.constants import IMG_WELCOME, IMG_LOGO, DISCLAIMER
from bin.views.constants import CENTER
from bin.template.menu_bar import MenuBar

class WelcomeView(FloatLayout):
    def __init__(self, **kwargs):
        self.app = kwargs.pop('app')
        super().__init__(**kwargs)
        self.pos_hint = CENTER
        
        img1 = b64toki(IMG_WELCOME)
        img1.fit_mode = 'cover'
        img1.pos_hint = CENTER
        
        self.add_widget(img1)
        
        img = b64toki(IMG_LOGO)
        img.size_hint = (0.3,0.3)
        img.pos_hint = {
            'center_x': .5,
            'center_y': .8
        }
        
        self.add_widget(img)
        
        label = Label(text=DISCLAIMER)
        self.add_widget(label)
        
        btn = Button(
            text = 'Start',
            bold = True,
            background_color = '33cccc',
            background_normal = ''
        )
        btn.size_hint = (0.2,0.1)
        btn.pos_hint = {
            'center_x': .5,
            'center_y': .1 
        }
        btn.bind(on_press=self.test)
        self.add_widget(btn)
        
        btn = Button(
            text = 'Open Video',
            bold = True,
            background_color = '33cccc',
            background_normal = ''
        )
        btn.size_hint = (0.2,0.1)
        btn.pos_hint = {
            'center_x': .5,
            'center_y': .3 
        }
        btn.bind(on_press=self.start_video)
        self.add_widget(btn)
    def start_video(self, *_):
        self.app.screen_manager.current = 'videoView'
    def test(self, *_):
        print('This worked')
        self.app.screen_manager.current = 'testView'