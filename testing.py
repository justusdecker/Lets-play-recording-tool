import pytest
from bin.data_access import *
from bin.automations import deploy

lp = LetsPlay('lets_plays.csv')

ep = Episode('eps_schedule_one.csv')

deploy(lp,ep,0)