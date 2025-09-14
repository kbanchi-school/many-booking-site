from peewee import *

db = SqliteDatabase('many_booking.db')

class Person(Model):
    name = CharField()
    age = IntegerField()

    class Meta:
        database = db # This model uses the "people.db" database.

db.create_tables([Person])
