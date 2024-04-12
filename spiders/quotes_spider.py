
import requests
from bs4 import BeautifulSoup
import json
import concurrent.futures
from pathlib import Path

from config import BASE_URL, QUOTES_DUMMY_DATA_PATH, AUTHORS_DUMMY_DATA_PATH

quotes = []
authors = []


def get_soup(url):
    response = requests.get(BASE_URL + url)
    return BeautifulSoup(response.text, 'lxml')


def get_quotes(page_url="/"):
    print('getting quotes from page ...', page_url)
    soup = get_soup(page_url)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for q in soup.find_all('div', class_='quote'):
            quote = dict()
            quote['quote'] = q.find('span', class_='text').get_text()
            quote['author'] = q.find('small', class_='author').get_text()
            quote['tags'] = [tag.get_text()
                             for tag in q.find_all('a', class_='tag')]

            quotes.append(quote)

            author_link = q.find('a').get('href')

            if (author_link):
                executor.submit(get_author_info, author_link)

    next_link = soup.find('li', class_='next')

    if next_link:
        get_quotes(next_link.find('a').get('href'))


def get_author_info(author_url):
    print('getting author info ...', author_url)
    soup = get_soup(author_url)

    author = dict()
    author['fullname'] = soup.find('h3', class_='author-title').get_text()
    author['born_date'] = soup.find(
        'span', class_='author-born-date').get_text()
    author['born_location'] = soup.find(
        'span', class_='author-born-location').get_text()
    author['description'] = soup.find(
        'div', class_='author-description').get_text().strip()

    authors.append(author)


def write_content_to_json():
    with open(QUOTES_DUMMY_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(quotes, f,  ensure_ascii=False, indent=2)
    with open(AUTHORS_DUMMY_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(authors, f,  ensure_ascii=False, indent=2)


def run_quotes_spider():
    get_quotes()
    write_content_to_json()


if __name__ == '__main__':
    run_quotes_spider()
