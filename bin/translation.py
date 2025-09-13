from os import listdir
from json import load
TRANSLATIONS = {}

def get_translations() -> dict[str,dict]:
    translations = {}
    for translation in listdir('./bin/data/lang/'):
        key = translation.split('.')[0]
        with open(f'./bin/data/lang/{translation}') as f:
            translations[key] = load(f)
        
TRANSLATIONS = get_translations()
def gtran(key,lang='en') -> str:
    TRANSLATIONS[lang].get(key,TRANSLATIONS[lang]['en'])