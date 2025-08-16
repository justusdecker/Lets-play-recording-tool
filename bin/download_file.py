import requests
def download_file(url: str, filepath: str):
    r = requests.get(url, allow_redirects=True)
    with open(filepath, 'wb') as file:
        file.write(r.content)