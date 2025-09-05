
def file_read(filepath : str) -> str:
    """Reads the entire content of a text file into a single string."""
    with open(filepath, 'r') as f:
        return f.read()

def file_write(filepath : str, data : str):
    """
    Writes a string to a text file.

    This function overwrites the file if it already exists.
    """
    with open(filepath, 'w') as f:
        f.write(data)
        
from subprocess import run
_, OVER = file_read('bin\\version.py').split(' = ')
OVER = OVER.replace("'",'')
MAJOR, MINOR, MICRO = OVER.split('.')
MICRO = str(int(MICRO) + 1)
VERSION = f"VERSION = '{MAJOR}.{MINOR}.{MICRO}'"
CH = run("git log --pretty=format:'%h' -n 1", capture_output=True, text=True).stdout.replace("\'",'')
CH = f'HASH = \"{CH}\"'
file_write('bin\\commit_hash.py',CH)
file_write('bin\\version.py',VERSION)

run('git add -A')
run(f'git commit -m {OVER}')
run(f'git push')
