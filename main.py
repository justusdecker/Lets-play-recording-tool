VERSION = '2.0.12'


from src.api.kivy_modules import *

from kivy.properties import ObjectProperty
from src.api.module_loader import DatabaseLoader



Builder.load_file('./src/api/application/main.kv')

import module.main as main_overwrite #! Try / Except this later: Building otherwise the build process will fail

Builder.load_file('./module/extension.kv') #! Try / Except this later: Building otherwise the build process will fail
main_overwrite.start()

class LPEPSub(BoxLayout):
    ...

class MenuSub(BoxLayout):
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

