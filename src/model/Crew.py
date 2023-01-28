import datetime

from peewee import *

from src.model.BaseModel import BaseModel


class Crew(BaseModel):
    """
    Crew class
    """
    id = PrimaryKeyField()
    name = CharField(unique=True)
    creation_date = DateTimeField(default=datetime.datetime.now)
    can_accept_new_members = BooleanField(default=True)
    is_active = BooleanField(default=True)
    disband_date = DateTimeField(null=True)

    class Meta:
        db_table = 'crew'
