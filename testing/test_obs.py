import pytest
from bin.obs import OBSObserver

def test_connection():
    """
    Make sure you have OBS open!
    """
    OBSO = OBSObserver()
    assert OBSO.isconnected