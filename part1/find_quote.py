from models import Quote, Author
import connect

import redis
from redis_lru import RedisLRU


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def print_results(func):
    def wrapper(name):
        results = func(name)

        if isinstance(results, list):
            print('Quotes:')
            for quote in results:
                print(quote)

        if isinstance(results, dict):
            for author, quotes in results.items():
                print(author)
                for quote in quotes:
                    print(quote)
    return wrapper


@cache
@print_results
def find_by_author_name(name: 'str'):
    authors = Author.objects(fullname__iregex=name)

    results = {}

    for a in authors:
        quotes = Quote.objects(author=a)
        results[a.fullname] = [q.quote for q in quotes]

    return results


@cache
@print_results
def find_by_tag(tag: 'str'):
    quotes = Quote.objects(tags__iregex=tag)

    return [q.quote for q in quotes]


@cache
@print_results
def find_by_tags(tags: [str]):
    quotes = Quote.objects(tags__in=tags.split(','))

    return [q.quote for q in quotes]


if __name__ == '__main__':
    INVALID_COMMAND_MESSAGE = 'Invalid choice. Possible choices are name:name; tag:tag; tags: tag, tab; exit.'

    commands = {
        'name': find_by_author_name,
        'tag': find_by_tag,
        'tags': find_by_tags
    }

    while True:
        user_input = input('Enter your choice: ')

        if user_input == 'exit':
            break

        if ':' not in user_input:
            print(INVALID_COMMAND_MESSAGE)
            continue

        command, args = user_input.split(':')

        func = commands.get(command)

        if func:
            func(args)  # Call the function with args
        else:
            print(INVALID_COMMAND_MESSAGE)
