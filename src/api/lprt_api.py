from requests import get
from requests.exceptions import HTTPError, RequestException

VERSION = None 
raise NotImplementedError()

def get_newest_version_number():
    """ Gets the newest version number Major.Minor Format """
    try:
        r = get('https://justusdecker.pythonanywhere.com/api/version')
        r.raise_for_status()
        return r.json()
    except (HTTPError, RequestException) as E:
        return {'version': '_'.join(VERSION.split('.')[0:2])}