import pytest
import obsws_python as obsws
def test_connection():
    obsws.ReqClient(host="localhost", port="8080", password="NOPE",timeout=1)