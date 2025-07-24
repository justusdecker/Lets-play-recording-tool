from subprocess import run, CREATE_NO_WINDOW
from bin.constants import TEMP_FOLDER
# FFMPEG Command Definitions

# FFMPEG_DEFAULT: Base command list for FFmpeg operations.
# - 'ffmpeg': The FFmpeg executable.
# - '-v quiet': Suppresses verbose output, showing only critical information.
# - '-stats': Displays encoding progress statistics.
# - '-loglevel error': Sets the logging level to show only error messages.
# - '-y': Overwrites output files without asking for confirmation.
FFMPEG_DEFAULT = ['ffmpeg', '-v', 'quiet', '-stats' , '-loglevel', 'error', '-y']

# FFMPEG_CONVERT_AUDIO_TYPE: Command to convert an audio file's type.
# - '__IN__': Placeholder for the input audio file path.
# - '__OUT__': Placeholder for the output audio file path.
FFMPEG_CONVERT_AUDIO_TYPE = [*FFMPEG_DEFAULT, '-i', '__IN__', '__OUT__']

# FFMPEG_EXTRACT: Command to extract two audio tracks from a video file.
# - '__IN__': Placeholder for the input video file path.
# - '-map 0:a:0': Selects the first audio stream from the input.
# - '-c:a copy': Copies the audio stream without re-encoding (lossless).
# - '__OUT1__': Placeholder for the output path of the first extracted audio track.
# - '-map 0:a:1': Selects the second audio stream from the input.
# - '-c:a copy': Copies the audio stream without re-encoding.
# - '__OUT2__': Placeholder for the output path of the second extracted audio track.
FFMPEG_EXTRACT = [*FFMPEG_DEFAULT, '-i', '__IN__', '-map', '0:a:0', '-c:a', 'copy', '__OUT1__', '-map', '0:a:1', '-c:a', 'copy','__OUT2__']

# FFMPEG_OPTIMIZED_EXTRACT: Identical to FFMPEG_EXTRACT, likely for clarity or
# future differentiation if optimization parameters were to be added.
# - Functionally the same as FFMPEG_EXTRACT.
FFMPEG_OPTIMIZED_EXTRACT = [*FFMPEG_DEFAULT, '-i', '__IN__', '-map', '0:a:0', '-c:a', 'copy', '__OUT1__', '-map',  '0:a:1', '-c:a', 'copy', '__OUT2__']

# FFMPEG_AUDIO_COMBINE: Command to combine two audio tracks into one, with volume control.
# - '__IN1__': Placeholder for the path of the first input audio file.
# - '__IN2__': Placeholder for the path of the second input audio file.
# - '-filter_complex': Starts a complex filtergraph.
#   - '[0:0]volume=__VOLUME1__[a]': Applies volume '__VOLUME1__' to the first input's first audio stream, labels it 'a'.
#   - '[1:0]volume=__VOLUME2__[b]': Applies volume '__VOLUME2__' to the second input's first audio stream, labels it 'b'.
#   - '[a][b]amix=inputs=2:duration=longest': Mixes streams 'a' and 'b', ensuring the output duration matches the longest input.
# - '__OUT__': Placeholder for the output combined audio file path.
FFMPEG_AUDIO_COMBINE = [*FFMPEG_DEFAULT, '-i', "__IN1__", '-i', "__IN2__", '-filter_complex', '[0:0]volume=__VOLUME1__[a];[1:0]volume=__VOLUME2__[b];[a][b]amix=inputs=2:duration=longest', "__OUT__"]

# FFMPEG_AUDIO_COMBINE_TRUNCATED: Command to combine two audio tracks, truncated to the first 2 minutes, with volume control.
# - '-ss 00:00:00': Starts input processing from the beginning.
# - '-to 00:02:00': Processes input up to 2 minutes.
# - '__IN1__': Placeholder for the path of the first input audio file.
# - '__IN2__': Placeholder for the path of the second input audio file.
# - '-filter_complex': Starts a complex filtergraph.
#   - '[0:0]volume=__VOLUME1__[a]': Applies volume '__VOLUME1__' to the first input's first audio stream, labels it 'a'.
#   - '[1:0]volume=__VOLUME2__[b]': Applies volume '__VOLUME2__' to the second input's first audio stream, labels it 'b'.
#   - '[a][b]amix=inputs=2:duration=longest': Mixes streams 'a' and 'b', ensuring the output duration matches the longest input.
# - '__OUT__': Placeholder for the output combined audio file path.
FFMPEG_AUDIO_COMBINE_TRUNCATED = [*FFMPEG_DEFAULT, '-ss' ,'00:00:00', '-to', '00:02:00', '-i', "__IN1__", '-ss' ,'00:00:00', '-to', '00:02:00', '-i', "__IN2__", '-filter_complex', '[0:0]volume=__VOLUME1__[a];[1:0]volume=__VOLUME2__[b];[a][b]amix=inputs=2:duration=longest', "__OUT__"] # '-ac', '2', amerge=inputs=2

# FFMPEG_AUDIO_PF_LN_L: Command to apply a series of audio filters (processing chain).
# - '__IN__': Placeholder for the input audio file path.
# - '-af': Specifies an audio filtergraph.
#   - 'highpass=f=175': Applies a high-pass filter with a cutoff frequency of 175 Hz.
#   - 'lowpass=f=13000': Applies a low-pass filter with a cutoff frequency of 13000 Hz.
#   - 'loudnorm=-15': Applies loudness normalization to -15 LUFS (Loudness Units Full Scale).
#   - 'compand=...': Applies a dynamic range compression/expansion filter with specific parameters.
# - '__OUT__': Placeholder for the output processed audio file path.
FFMPEG_AUDIO_PF_LN_L = [*FFMPEG_DEFAULT, '-i', '__IN__', '-af','highpass=f=175, lowpass=f=13000, loudnorm=-15, compand=0|0:1|1:0/-3|10/-3|20/-3:0.1:0:0:0', '__OUT__']

# FFMPEG_VIDEO_RENDER: Command to combine a video stream with an audio stream.
# - '-an': Disables audio from the first input (video).
# - '__VIDEO__': Placeholder for the input video file path.
# - '__AUDIO__': Placeholder for the input audio file path.
# - '-map 0:v': Selects the video stream from the first input.
# - '-map 1:a': Selects the audio stream from the second input.
# - '-c:v copy': Copies the video stream without re-encoding.
# - '-c:a copy': Copies the audio stream without re-encoding.
# - '__OUTPUT__': Placeholder for the final output video file path.
FFMPEG_VIDEO_RENDER = [*FFMPEG_DEFAULT, '-an', '-i', '__VIDEO__', '-i', '__AUDIO__', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '__OUTPUT__']

# FFMPEG_GET_FRAME: Command to extract a single frame (thumbnail) from a video at a specific time.
# - '-ss __TIME__': Seeks to the specified time (e.g., '00:00:05' for 5 seconds).
# - '__IN__': Placeholder for the input video file path.
# - '-frames:v 1': Extracts only one video frame.
# - 'temp.png': The output file name for the extracted frame.
FFMPEG_GET_FRAME = [*FFMPEG_DEFAULT, '-ss', '__TIME__', '-i', '__IN__', '-frames:v', '1', f'{TEMP_FOLDER}temp.png']

# FFMPEG_GET_LENGTH: Command (using ffprobe) to get the duration of a video stream.
# - 'ffprobe': The FFprobe executable (part of the FFmpeg suite).
# - '-v error': Suppresses verbose output, showing only errors.
# - '-select_streams v:0': Selects the first video stream.
# - '-show_entries stream=duration': Shows only the duration entry for the stream.
# - '-of default=noprint_wrappers=1:nokey=1': Formats the output to show only the value (duration) without keys or wrappers.
# - '__IN__': Placeholder for the input video file path.
FFMPEG_GET_LENGTH = ['ffprobe', '-v', 'error', '-select_streams', 'v:0','-show_entries', 'stream=duration', '-of', 'default=noprint_wrappers=1:nokey=1', '__IN__']


def ffmpeg_exists() -> bool:
    """
    Checks if the FFmpeg executable is accessible in the system's PATH.

    This function attempts to run a basic 'ffmpeg' command and then inspects
    its standard output to determine if the string '\"ffmpeg\"' is *not* present.
    The presence of this string in the output is used as an indicator that the
    command was not found by the system's command interpreter.

    Returns:
        bool: True if 'ffmpeg' appears to be found and executable, False otherwise.

    !Note: See issue #106
    """
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

def ffmpeg_run(cmd: list[list], replacer: dict[str,str]={},nr: bool = False):
    """
    This function runs your FFMPEG command. Before this happens this function calls ffmpeg_build to replace some essential variables.
    
    Subprocess is used to call FFMPEG
    
    The settings are: NO WINDOW <- Don't work with terminal applications!
    
    shell= True is compatible with limiter compand
    """
    if nr:
        return run(ffmpeg_build(cmd,replacer), CREATE_NO_WINDOW, capture_output=True, text=True).stdout
    else:
        try:
            run(ffmpeg_build(cmd,replacer), CREATE_NO_WINDOW,)
            return True
        except FileNotFoundError:
            return None
from tkinter.messagebox import showerror
from bin.constants import ERROR_010, ERROR_011, ERROR_012     
if ffmpeg_run(['ffmpeg']) is None:
    showerror('ERROR', ERROR_010)
    quit()
if ffmpeg_run(['ffplay']) is None:
    showerror('ERROR', ERROR_011)
    quit()
#if ffmpeg_run(['ffprobe']) is None: Not in use currently
#    showerror('ERROR', ERROR_010)
#    quit()