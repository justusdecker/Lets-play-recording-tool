"""

# Functions

### `ffmpeg_exists()`
This function checks if the FFmpeg executable is accessible on the system's PATH. It runs a simple `ffmpeg` command and analyzes the output to confirm the command was found and executed, rather than returning an error indicating it wasn't recognized.

### `ffmpeg_build(cmd: list[str], replacer: dict[str, str])`
This function takes an FFmpeg command list (`cmd`) and a dictionary of key-value pairs (`replacer`). It iterates through the command and replaces all placeholders (e.g., `__IN__`, `__OUT__`) with their corresponding values from the dictionary. Forgetting to replace a key will cause an error when FFmpeg is executed.

### `ffmpeg_run(cmd: list[str], replacer: dict[str, str] = {}, nr: bool = False)`
This is the main function for executing FFmpeg commands.
1.  It first calls `ffmpeg_build()` to prepare the command by replacing all necessary variables.
2.  Then, it uses Python's `subprocess` module to run the command.
3.  The `nr=True` parameter tells the function to **return the console output** from the command. If `nr=False` (the default), it simply executes the command and waits for it to finish.
4.  If the FFmpeg executable is not found, the function catches the `FileNotFoundError` and returns `None`.

# FFMPEG Command Definitions

.. FFMPEG_DEFAULT:: 
    Base command list for FFmpeg operations.
    ***
    `'ffmpeg'`:
        The FFmpeg executable.
    `'-y'`:
        Overwrites output files without asking for confirmation.

.. FFMPEG_DEFAULT_PRODUCTION::
    Base command for production environments.
    ***
    `'ffmpeg'`:
        The FFmpeg executable.
    `'-v quiet'`:
        Suppresses verbose output.
    `'-stats'`:
        Displays encoding progress statistics.
    `'-loglevel error'`:
        Sets logging level to show only errors.
    `'-y'`:
        Overwrites output files without confirmation.

.. FFMPEG_CONVERT_AUDIO_TYPE::
    Command to convert an audio file's format.
    ***
    `'-i __IN__'`
        Specifies the input audio file path.
    `'__OUT__'`
        Specifies the output audio file path.

.. FFMPEG_EXTRACT::
    Command to extract two audio tracks from a video file.
    ***
    `'-i __IN__'`
        Specifies the input video file.
    `'-map 0:a:0'`:
        Selects the first audio stream from the input file.
    `'-c:a copy'`:
        Copies the audio stream without re-encoding (lossless).
    `'__OUT1__'`
        Path for the first extracted audio track.
    `'-map 0:a:1'`:
        Selects the second audio stream.
    `'__OUT2__'`
        Path for the second extracted audio track.

.. FFMPEG_OPTIMIZED_EXTRACT::
    Identical to FFMPEG_EXTRACT, for extracting two audio tracks.
    ***
    `'-i __IN__'`
        Specifies the input video file.
    `'-map 0:a:0'`:
        Selects the first audio stream.
    `'-c:a copy'`:
        Copies the audio stream losslessly.
    `'__OUT1__'`
        Path for the first extracted audio track.
    `'-map 0:a:1'`:
        Selects the second audio stream.
    `'__OUT2__'`
        Path for the second extracted audio track.

.. FFMPEG_AUDIO_COMBINE::
    Command to combine two audio tracks with individual volume control.
    ***
    `'-i __IN1__'`
        Path for the first input audio file.
    `'-i __IN2__'`
        Path for the second input audio file.
    `'-filter_complex'`:
        Starts a complex filtergraph.
    `'[0:0]volume=__VOLUME1__[a]'`:
        Applies a volume level to the first input and labels it 'a'.
    `'[1:0]volume=__VOLUME2__[b]'`:
        Applies a volume level to the second input and labels it 'b'.
    `'[a][b]amix=inputs=2:duration=longest'`:
        Mixes the two labeled streams, with the output duration matching the longest input.
    `'__OUT__'`
        Path for the final combined audio file.

.. FFMPEG_AUDIO_COMBINE_TRUNCATED::
    Combines two audio tracks, truncating them to the first 2 minutes, with volume control.
    ***
    `'-ss 00:00:00 -to 00:02:00'`:
        Specifies the input range from the start to 2 minutes.
    `'-i __IN1__'`
        Path for the first input audio file.
    `'-i __IN2__'`
        Path for the second input audio file.
    `'-filter_complex'`:
        Starts a complex filtergraph.
    `'[0:0]volume=__VOLUME1__[a]'`:
        Applies volume to the first input, labels it 'a'.
    `'[1:0]volume=__VOLUME2__[b]'`:
        Applies volume to the second input, labels it 'b'.
    `'[a][b]amix=inputs=2:duration=longest'`:
        Mixes the streams, duration matches the longest truncated input.
    `'__OUT__'`
        Path for the final combined audio file.

.. FFMPEG_AUDIO_PF_LN_L::
    Applies a specific chain of audio filters to an input file.
    ***
    `'-i __IN__'`
        Path for the input audio file.
    `'-af __FILTERS__'`
        Specifies an audio filtergraph. The placeholder `__FILTERS__` will be replaced with a string like `'highpass=f=175,lowpass=f=13000,loudnorm=I=-15:TP=-1.5:LRA=11'`.
    `'__OUT__'`
        Path for the output audio file.

.. FFMPEG_VIDEO_RENDER::
    Combines a video stream and an audio stream into a single file.
    ***
    `'-an'`:
        Disables audio from the first input.
    `'-i __VIDEO__'`
        Path for the input video file.
    `'-i __AUDIO__'`
        Path for the input audio file.
    `'-map 0:v'`:
        Selects the video stream from the first input.
    `'-map 1:a'`:
        Selects the audio stream from the second input.
    `'-c:v copy'`:
        Copies the video stream without re-encoding (lossless).
    `'-c:a copy'`:
        Copies the audio stream without re-encoding (lossless).
    `'__OUTPUT__'`
        Path for the final output video file.

.. FFMPEG_GET_FRAME::
    Extracts a single frame (thumbnail) from a video at a specific time.
    ***
    `'-ss __TIME__'`
        Seeks to the specified time (e.g., '00:00:05').
    `'-accurate_seek'`:
        Ensures a precise seek to the specified timestamp.
    `'-i __IN__'`
        Path for the input video file.
    `'-frames:v 1'`:
        Extracts exactly one video frame.
    `'temp.png'`
        The output file name for the frame, saved in the temporary folder.

.. FFMPEG_GET_LENGTH::
    Uses FFprobe to get the duration of a video stream.
    ***
    `'ffprobe'`:
        The FFprobe executable.
    `'-v error'`:
        Suppresses verbose output.
    `'-select_streams v:0'`:
        Selects the first video stream.
    `'-show_entries stream=duration'`:
        Shows only the duration of the stream.
    `'-of default=noprint_wrappers=1:nokey=1'`:
        Formats the output to show only the duration value.
    `'__IN__'`
        Path for the input video file.

.. FFMPEG_GET_STREAM_AMOUNT::
    Uses FFprobe to get the total number of streams in a file.
    ***
    `'ffprobe'`:
        The FFprobe executable.
    `'-v error'`:
        Suppresses verbose output.
    `'-show_entries format=nb_streams'`:
        Shows the number of streams in the file format.
    `'-of default=noprint_wrappers=1:nokey=1'`:
        Formats the output to show only the number of streams.
    `'__IN__'`
        Path for the input file.
"""


from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')
from subprocess import run, CREATE_NO_WINDOW
from bin.constants import TEMP_FOLDER

#['ffmpeg', '-y'] <- default debug

FFMPEG_DEFAULT_PRODUCTION = ['ffmpeg', '-y']

FFMPEG_DEFAULT = ['ffmpeg', '-v', 'quiet', '-stats' , '-loglevel', 'error', '-y']

FFMPEG_CONVERT_AUDIO_TYPE = [*FFMPEG_DEFAULT, '-i', '__IN__', '__OUT__']

FFMPEG_EXTRACT = [*FFMPEG_DEFAULT, '-i', '__IN__', '-map', '0:a:0', '-c:a', 'copy', '__OUT1__', '-map', '0:a:1', '-c:a', 'copy','__OUT2__']

FFMPEG_OPTIMIZED_EXTRACT = [*FFMPEG_DEFAULT, '-i', '__IN__', '-map', '0:a:0', '-c:a', 'copy', '__OUT1__', '-map',  '0:a:1', '-c:a', 'copy', '__OUT2__']

FFMPEG_AUDIO_COMBINE = [*FFMPEG_DEFAULT, '-i', "__IN1__", '-i', "__IN2__", '-filter_complex', '[0:0]volume=__VOLUME1__[a];[1:0]volume=__VOLUME2__[b];[a][b]amix=inputs=2:duration=longest', "__OUT__"]

FFMPEG_AUDIO_COMBINE_TRUNCATED = [*FFMPEG_DEFAULT, '-ss' ,'00:00:00', '-to', '00:02:00', '-i', "__IN1__", '-ss' ,'00:00:00', '-to', '00:02:00', '-i', "__IN2__", '-filter_complex', '[0:0]volume=__VOLUME1__[a];[1:0]volume=__VOLUME2__[b];[a][b]amix=inputs=2:duration=longest', "__OUT__"] # '-ac', '2', amerge=inputs=2

FFMPEG_AUDIO_PF_LN_L = [*FFMPEG_DEFAULT, '-i', '__IN__', '-af','__FILTERS__', '__OUT__']

FFMPEG_VIDEO_RENDER = [*FFMPEG_DEFAULT, '-an', '-i', '__VIDEO__', '-i', '__AUDIO__', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '__OUTPUT__']

FFMPEG_GET_FRAME = [*FFMPEG_DEFAULT, '-ss', '__TIME__' , '-accurate_seek', '-i', '__IN__', '-frames:v', '1', f'{TEMP_FOLDER}temp.png']

FFMPEG_GET_LENGTH = ['ffprobe', '-v', 'error', '-select_streams', 'v:0','-show_entries', 'stream=duration', '-of', 'default=noprint_wrappers=1:nokey=1', '__IN__']

FFMPEG_GET_STREAM_AMMOUNT = ['ffprobe', '-v', 'error','-show_entries','format=nb_streams','-of','default=noprint_wrappers=1:nokey=1','__IN__']

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
from bin.download_file import download_ffmpeg  
if ffmpeg_run(['ffmpeg']) is None or ffmpeg_run(['ffplay']) is None or ffmpeg_run(['ffprobe']) is None:
    showerror('ERROR', 'No FFMPEG found!\nStart download!')
    download_ffmpeg()
    quit()
