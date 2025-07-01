import pytest
from bin.data_access import *
from bin.automations import deploy

ep = Episode('test.csv')
ep.add('test123')
ep.save()

#lp = LetsPlay('lets_plays.csv')

#ep = Episode('eps_schedule_one.csv')

#deploy(lp,ep,0)