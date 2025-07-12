from pygame.mixer import init, music

init()

def play_audio(filepath: str):
    music.load(filepath)
    music.play()

play_audio("C:\\Users\\Justus\\jri_data\\audio\\1_schedule_one_track_desktop.mp3")
while music.get_busy():
    print(music.get_pos())