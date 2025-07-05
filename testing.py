import pytest
from bin.constants import ffmpeg_run
from bin.audio import limiter
from bin.constants import FFMPEG_EXTRACT, FFMPEG_LOUDNESS_NORMALIZATION, FFMPEG_LIMITER
#limiter('test_1.mp3','test_2.mp3')
#ffmpeg_run(FFMPEG_LOUDNESS_NORMALIZATION,{'__IN__': 'test.mp3','__OUT__':'test_1.mp3'})
ffmpeg_run(FFMPEG_LIMITER,{'__IN__': 'test_1.mp3','__OUT__':'test_2.mp3'})
#ffmpeg_run(FFMPEG_EXTRACT,{'__IN__': 'C:/Users/Justus/Videos/2025-06-29 22-43-39.mp4','__OUT__':'test.mp3','__MAPPING__':'1'})