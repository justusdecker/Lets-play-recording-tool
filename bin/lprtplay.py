from pygame.mixer import init, music

init()

def play_audio(filepath: str):
    if music.get_busy():
        music.stop()
    
    music.load(filepath)
    music.play(loops=-1)

def stop_audio():
    if music.get_busy():
        music.stop()