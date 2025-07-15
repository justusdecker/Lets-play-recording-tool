from bin.constants import *



ffmpeg_run(FFMPEG_GET_FRAME,{'__IN__': 'C:/Users/Justus/Videos/requiem.mov', '__TIME__': '120.0'})

time = ffmpeg_run(FFMPEG_GET_LENGTH,{'__IN__':'C:/Users/Justus/Videos/requiem.mov'},True)

print(time)