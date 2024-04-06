import json
from config import AUTHORS_DUMMY_DATA_PATH, QUOTES_DUMMY_DATA_PATH
from part1.models import Author, Quote
import part1.connect as connect

with open(AUTHORS_DUMMY_DATA_PATH, "r", encoding="utf-8") as read_content:
    authors = json.load(read_content)
    for author in authors:
        try:
            print('creating author ...')

            author = Author(fullname=author['fullname'],
                            born_date=author['born_date'],
                            born_location=author['born_location'],
                            description=author['description'])
            author.save()
        except Exception as e:
            print('omitting author ...')

with open(QUOTES_DUMMY_DATA_PATH, "r", encoding="utf-8") as read_content:
    quotes = json.load(read_content)
    for quote in quotes:
        try:
            print('creating quote ...')
            author, *_ = Author.objects(fullname=quote.get('author'))
            quote = Quote(quote=quote.get('quote'),
                          author=author, tags=quote.get('tags'))
            quote.save()
        except Exception as e:
            print('error:', e)
            print('omitting quote ...')
