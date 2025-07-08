from pathlib import Path
# this will be needed to delete some temp files after a certain time
for path in Path('.').iterdir():
    info = path.stat()
    print(info)
input()