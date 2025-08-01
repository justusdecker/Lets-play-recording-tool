from bin.data_access import *
from random import randint as ri
for i in range(3):
    SQLAccess.create_letsplay(f'Lets Play {i}','XXX',ri(1200,1800))
    r = 10
    print(r)
    for j in range(r):
        SQLAccess.create_episode(i,f'{j}.mp4')
SQLAccess.delete_letsplay(0)
print(len(SQLAccess.read_episodes(0)))
#SQLAccess.delete_episode(0,1)
print(len(SQLAccess.read_episodes(0)))
print(len(SQLAccess.read_episodes(1)))
print(len(SQLAccess.read_episodes(2)))



SQLAccess.update_letsplay(0,146436)
SQLAccess.update_episodes(0,0,video_path = 'New Videopath')
print(SQLAccess.read_letsplays()[3].id)
#print(SQLAccess.read_episodes()[0].id)