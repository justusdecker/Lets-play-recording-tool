from json import load
from bin.ver import version
def jsr() -> dict | list:
    try:
        with open('./bin/pinfo.json', 'r') as f:
            v = load(f)
            return ".".join([str(v[i]) for i in v])
    except:
        return version

VERSION = jsr()