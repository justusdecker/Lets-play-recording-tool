from bin.views.modules import *
from bin.views.welcome import WelcomeView
from bin.views.letsplays import letsplayListView, letsplaySingleView

from bin.template.menu_bar import MenuBar


class videoView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        video = VideoPlayer(source='./test.mov',options={'fit_mode': 'contain'})
        self.add_widget(video)

class TestView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.menu = MenuBar(app=app)
        self.add_widget(self.menu)
        
        label = Label(text='Test', font_size= 30)
        self.add_widget(label)

class LPRTApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        
        self.welcome_view = WelcomeView(app=app)
        screen = Screen(name='welcomeView')
        screen.add_widget(self.welcome_view)
        self.screen_manager.add_widget(screen)
        
        self.test_view = TestView()
        screen = Screen(name='testView')
        screen.add_widget(self.test_view)
        self.screen_manager.add_widget(screen)
        
        self.db_view = letsplayListView(app=app)
        screen = Screen(name='letsplayListView')
        screen.add_widget(self.db_view)
        self.screen_manager.add_widget(screen)
        
        self.db2_view = letsplaySingleView(app=app)
        screen = Screen(name='letsplaySingleView')
        screen.add_widget(self.db2_view)
        self.screen_manager.add_widget(screen)
        
        self.video_view = videoView()
        screen = Screen(name='videoView')
        screen.add_widget(self.video_view)
        self.screen_manager.add_widget(screen)
        
        return self.screen_manager

if __name__ == '__main__':
    app = LPRTApp()
    app.run()
