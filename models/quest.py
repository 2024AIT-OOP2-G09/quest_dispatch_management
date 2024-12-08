from peewee import Model, ForeignKeyField, DateTimeField, CharField
from .db import db
from .character import Character
from .weapon import Weapon

class Quest(Model):
    name = CharField()
    character = ForeignKeyField(Character, backref='quests')
    weapon = ForeignKeyField(Weapon, backref='quests')
    quest_date = DateTimeField()

    class Meta:
        database = db