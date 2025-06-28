import pytest
from bin.thumbnail import ThumbnailGenerator
def test_create_tg():
    ThumbnailGenerator()
def test_create_thumbnail():
    TG = ThumbnailGenerator()
    TG.generate('123','test.mp4','tad_test.json','test.png',0)
def test_create_thumbnail_random_image():
    TG = ThumbnailGenerator()
    TG.generate('123','test.mp4','tad_test.json','test.png',-1)