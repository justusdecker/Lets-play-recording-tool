
from src.api import TkinterApp, AddView
from module.module_main import Recording, FetchAudio
AddView(Recording)
AddView(FetchAudio)
if __name__ == '__main__':
    APP = TkinterApp()
    APP.mainloop()
     
    
