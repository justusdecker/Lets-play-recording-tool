from bin.views.modules import *
from bin.views.letsplays import letsplayListView, letsplaySingleView
from kivy.properties import ObjectProperty

from bin.template.menu_bar import MenuBar

Builder.load_file('./application/main.kv')

class MenuSub(BoxLayout):
    ...

class OBSView(BoxLayout):
    ...

class WelcomeView(FloatLayout):
    """
    The Startup View.
    """
    def start_app(self, *_):
        print('This worked')
        app.screen_manager.current = 'testView'
        


class MainWidget(FloatLayout):
    manager = ObjectProperty(None)
    ...

class LPRTApp(App):
    screen_manager = ObjectProperty(None)
    def build(self):
        root = MainWidget()
        self.screen_manager = root.ids.screen_manager
        
        return root

if __name__ == '__main__':

    app = LPRTApp()
    app.run()

