from bin.constants import *



ffmpeg_run(FFMPEG_GET_FRAME,{'__IN__': 'C:/Users/Justus/Videos/requiem.mov', '__TIME__': '120.0'})

time = ffmpeg_run(FFMPEG_GET_LENGTH,{'__IN__':'C:/Users/Justus/Videos/requiem.mov'},True)

def get_time_va(filepath: str):
    time_or_error = ffmpeg_run(FFMPEG_GET_LENGTH,{'__IN__':filepath},True)
    try:
        return float(time_or_error.replace('\n',''))
    except :
        return None
print(get_time_va('C:/Users/Justus/Videos/requiem.mov'))