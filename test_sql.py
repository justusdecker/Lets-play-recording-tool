from bin.data_access_new import *
SQLAccess.create_letsplay('minecraft hardcore','minecraft_hardcore',1800)
SQLAccess.create_episode(1,'123.mp4')
print(SQLAccess.read_letsplays()[3].id)
#print(SQLAccess.read_episodes()[0].id)