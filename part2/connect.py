from mongoengine import connect
print('connecting to database ...')
connect(
    host=f"""mongodb+srv://admin:admin@cluster0.zjuiwy3.mongodb.net/
test?retryWrites=true&w=majority""", ssl=True)
