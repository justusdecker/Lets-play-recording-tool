import pytest
from bin.resolve_sender import DaviniciSender

def test_handshake():
    DS = DaviniciSender()
    DS.send_to_davinci('<HANDSHAKE>')