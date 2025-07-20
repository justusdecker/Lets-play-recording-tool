from subprocess import run, CREATE_NO_WINDOW

FFMPEG_DEFAULT = ['ffmpeg', '-v', 'quiet', '-stats' , '-loglevel', 'error', '-y']

FFMPEG_CONVERT_AUDIO_TYPE = [*FFMPEG_DEFAULT, '-i', '__IN__', '__OUT__']

FFMPEG_EXTRACT = [*FFMPEG_DEFAULT, '-i', '__IN__', '-map', '0:a:0', '-c:a', 'copy', '__OUT1__', '-map', '0:a:1', '-c:a', 'copy','__OUT2__']

FFMPEG_OPTIMIZED_EXTRACT = [*FFMPEG_DEFAULT, '-i', '__IN__', '-map', '0:a:0', '-c:a', 'copy', '__OUT1__', '-map',  '0:a:1', '-c:a', 'copy', '__OUT2__']

FFMPEG_AUDIO_COMBINE = [*FFMPEG_DEFAULT, '-i', "__IN1__", '-i', "__IN2__", '-filter_complex', '[0:0]volume=__VOLUME1__[a];[1:0]volume=__VOLUME2__[b];[a][b]amix=inputs=2:duration=longest', "__OUT__"]

FFMPEG_AUDIO_COMBINE_TRUNCATED = [*FFMPEG_DEFAULT, '-ss' ,'00:00:00', '-to', '00:02:00', '-i', "__IN1__", '-ss' ,'00:00:00', '-to', '00:02:00', '-i', "__IN2__", '-filter_complex', '[0:0]volume=__VOLUME1__[a];[1:0]volume=__VOLUME2__[b];[a][b]amix=inputs=2:duration=longest', "__OUT__"] # '-ac', '2', amerge=inputs=2

FFMPEG_AUDIO_PF_LN_L = [*FFMPEG_DEFAULT, '-i', '__IN__', '-af','highpass=f=175, lowpass=f=13000, loudnorm=-15, compand=0|0:1|1:0/-3|10/-3|20/-3:0.1:0:0:0', '__OUT__']

FFMPEG_VIDEO_RENDER = [*FFMPEG_DEFAULT, '-an', '-i', '__VIDEO__', '-i', '__AUDIO__', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '__OUTPUT__']

FFMPEG_GET_FRAME = [*FFMPEG_DEFAULT, '-ss', '__TIME__', '-i', '__IN__', '-frames:v', '1', 'temp.png']

FFMPEG_GET_LENGTH = ['ffprobe', '-v', 'error', '-select_streams', 'v:0','-show_entries', 'stream=duration', '-of', 'default=noprint_wrappers=1:nokey=1', '__IN__']


def ffmpeg_exists() -> bool:
    _ret = run('ffmpeg', CREATE_NO_WINDOW, capture_output=True, text=True).stdout
    return '\"ffmpeg\"' not in _ret
        

def ffmpeg_build(cmd: list[str], replacer: dict[str,str]):
    """
    This function takes the FFMPEG command and replaces all of the keys that can be found in the command!
    
    If you forget to change a key, this will result in an error from FFMPEG. No Exception raises.
    
    Is a key not existent it will replace nothing.
    """
    for key in replacer:
        cmd = [arg.replace(key,str(replacer[key])) if key in arg else arg for arg in cmd]
    return cmd

def ffmpeg_run(cmd: list[list], replacer: dict[str,str],nr: bool = False):
    """
    This function runs your FFMPEG command. Before this happens this function calls ffmpeg_build to replace some essential variables.
    
    Subprocess is used to call FFMPEG
    
    The settings are: NO WINDOW <- Don't work with terminal applications!
    
    shell= True is compatible with limiter compand
    """
    if nr:
        return run(ffmpeg_build(cmd,replacer), CREATE_NO_WINDOW, capture_output=True, text=True).stdout
    else:
        run(ffmpeg_build(cmd,replacer), CREATE_NO_WINDOW,)