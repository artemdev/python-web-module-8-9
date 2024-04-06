from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    name = StringField(max_length=50)
    email = BooleanField(default=False)
    phone = StringField(max_length=15)
    preferred_contact_method = StringField(max_length=5, default='email')
    meta = {"collection": 'contacts'}
