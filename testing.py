import pytest
from bin.constants import ffmpeg_run
from bin.constants import FFMPEG_EXTRACT

ffmpeg_run(FFMPEG_EXTRACT,{'__IN__': 'C:/Users/Justus/Videos/2025-06-29 22-43-39.mp4','__OUT__':'test.mp3','__MAPPING__':'1'})