from json import load
def jsr() -> dict | list:
    with open('./bin/pinfo.json', 'r') as f:
        v = load(f)
        return ".".join([str(v[i]) for i in v])

VERSION = jsr()