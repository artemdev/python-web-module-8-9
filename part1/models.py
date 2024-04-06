from mongoengine import Document
from mongoengine import ReferenceField, ListField, StringField, CASCADE


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": 'authors'}


class Quote(Document):
    quote = StringField()
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    meta = {"collection": 'quotes'}
