from os.path import isfile
with open('episodes_export.csv') as f:
    idx = 0
    for line in f.read().splitlines():
        if line.startswith('valheim'):
            file = line.split('|')[4]
            
            print(idx,file,isfile(file))
            idx += 1