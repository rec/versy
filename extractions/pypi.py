
# import safer
from bs4 import BeautifulSoup
import requests

URL = (
    'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.json'
)


def get_projects(url=URL):
    return [row['project'] for row in requests.get(url).json()['rows']]


def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, features='html.parser')


def get_pypi(project):
    get_soup('https://pypi.org/project/' + project)


def get_links(soup):
    links = soup.find_all('a')

    links = ((i.get('href'), i) for i in soup.find_all('a'))
    links = ((h, t) for h, t in links if h and h.startswith('http'))

    return links


def main():
    soup = get_pypi('safer')
    for h, t in get_links(soup):
        print(h)


if __name__ == '__main__':
    main()
