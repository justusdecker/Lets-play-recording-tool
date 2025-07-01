import pytest
from bin.data_access import *
from bin.automations import generate_markdown
def test_gen():
    lp = LetsPlay('lets_play.csv')
    
    ep = Episode('eps_schedule_one.csv')
    
    generate_markdown(lp,ep,0)