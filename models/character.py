from peewee import Model, CharField
from .db import db

class Character(Model):
    name = CharField()
    gender = CharField()

    class Meta:
        database = db