import subprocess

def render(vid,aud):
    """        
    """
    
    subprocess.run(
                (
                    'ffmpeg',
                    '-y',               # Will replace existing output
                    '-i',               # Input filepath 1
                    '-an',
                    f"{vid}",            # Input filepath 1
                    

                    '-i',               # Input filepath 2
                    f"{aud}",           # Input filepath 2
                    '-filter_complex',  #for merging
                    'amerge=inputs=2',  # For merging
                    '-ac', '2',         # Set audio channel
                    f"temp.mp3"         # output filepath
                    ),
                subprocess.CREATE_NO_WINDOW,
                shell= True
                )