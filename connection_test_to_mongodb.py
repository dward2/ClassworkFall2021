from pymodm import connect, MongoModel, fields

connect("mongodb+srv://<your_db_username>:<passwd>@bme547.ba348.mongodb.net/"
        "health_db?retryWrites=true&w=majority")


class User(MongoModel):
    name = fields.CharField()


x = User(name="David")
x.save()

# After running this code, visit MongoDB online to ensure new entry made.
