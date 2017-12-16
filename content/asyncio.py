import requests


def get_content(url):
    response = requests.get(url)
    return response.text
