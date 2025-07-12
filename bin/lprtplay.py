from pygame.mixer import init, music

init()

def play_audio(filepath: str):
    music.load(filepath)
    music.play()



"""
Pseudo code:

For noise in episode_noises:
    play_audio noise
    user input:
        ok  -> set the noise_file -> next episode
        not okay -> next audio noise -> Break Workflow if no audio existing anymore (later)
At the end:

For noise in okay_noise:
    sox create noise_profile with noise
    sox apply noise_profile
"""