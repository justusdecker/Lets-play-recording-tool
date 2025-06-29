import pytest
from bin.resolve_sender import DaviniciSender

def test_handshake_and_clean():
    DS = DaviniciSender()
    DS.send_to_davinci('handshake')
    assert DS.recv_from_user() == 'handshake'
    DS.clean(False)
    assert DS.recv_from_user() == ''