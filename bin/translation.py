from os import listdir
from json import load
TRANSLATIONS = {}
LANG = 'en'
def get_translations() -> dict:
    translations = {}
    for translation in listdir('./bin/data/lang/'):
        key = translation.split('.')[0]
        with open(f'./bin/data/lang/{translation}') as f:
            translations[key] = load(f)
    return translations
TRANSLATIONS = get_translations()
def gtran(key) -> str:
    return TRANSLATIONS[LANG].get(key,TRANSLATIONS['en'][key])