from pygame.mixer import init, music

init()

def play_audio(filepath: str):
    stop_audio()
    
    music.load(filepath)
    music.play(loops=-1)

def stop_audio():
    if music.get_busy():
        music.stop()
        music.unload()