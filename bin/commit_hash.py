from subprocess import run

HASH = run("git log --pretty=format:'%h' -n 1", capture_output=True, text=True).stdout.replace("\'",'')