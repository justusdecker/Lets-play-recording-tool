import pytest
from bin.constants import ffmpeg_run
from bin.audio import limiter
from bin.constants import *
#limiter('test_1.mp3','test_2.mp3')
for i in range(20):
    print()
#ffmpeg_run(FFMPEG_LOUDNESS_NORMALIZATION,{'__IN__': 'test.mp3','__OUT__':'test_1.mp3'})
#ffmpeg_run(FFMPEG_LIMITER,{'__IN__': 'test_1.mp3','__OUT__':'test_2.mp3'})
#ffmpeg_run(FFMPEG_EXTRACT,{'__IN__': 'C:/Users/Justus/Videos/2025-06-29 22-43-39.mp4','__OUT__':'test.mp3','__MAPPING__':'1'})
mic = "C:\\Users\\Justus\\jri_data\\audio\\1_schedule_one_track_mic.mp3"
desk = "C:\\Users\\Justus\\jri_data\\audio\\1_schedule_one_track_desktop.mp3"
#ffmpeg_run(FFMPEG_VOLUME_APPLIER,{'__IN__':desk,'__VOLUME__': str('0.5')})
ffmpeg_run(FFMPEG_AUDIO_COMBINE,{'__IN1__':mic,'__IN2__': desk,'__VOLUME1__': str(1.0),'__VOLUME2__': str(0.5),'__OUT__':'out.mp3'})
