import pytest
from bin.resolve_sender import DaviniciSender

def test_handshake_and_clean():
    DS = DaviniciSender()
    DS.send_to_davinci('handshake')
    assert DS.recv_from_user() == 'handshake'
    DS.clean(False)
    assert DS.recv_from_user() == ''
    
def test_create_timeline():
    DS = DaviniciSender()
    DS.send_to_davinci('import<C:/Users/Justus/Videos/2025-06-29 22-43-39.mp4<C:\\Users\\Justus\\jri_data\\audio\\1_schedule_one_final.mp3<1234')