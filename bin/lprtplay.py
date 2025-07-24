
try: #Fix for issue: #126
    from pygame.mixer import init, music
except:
    from tkinter.messagebox import showerror
    from bin.constants import ERROR_008
    showerror('ERROR', ERROR_008 + '\npygame')
    quit()


init()

def play_audio(filepath: str):
    stop_audio()
    
    music.load(filepath)
    music.play(loops=-1)

def stop_audio():
    if music.get_busy():
        music.stop()
        music.unload()