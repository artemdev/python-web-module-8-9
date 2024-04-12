from mongoengine import connect
print('connecting to database ...')
db = connect(
    db='test',
    host=f"""mongodb+srv://admin:admin@cluster0.zjuiwy3.mongodb.net/
test?retryWrites=true&w=majority""", ssl=True)

