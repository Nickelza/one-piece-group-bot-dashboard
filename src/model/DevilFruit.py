from peewee import *

from src.model.BaseModel import BaseModel
from src.model.GroupChat import GroupChat
from src.model.User import User
from src.model.enums.devil_fruit.DevilFruitStatus import DevilFruitStatus


class DevilFruit(BaseModel):
    """
    DevilFruit class
    """
    id = PrimaryKeyField()
    category = SmallIntegerField()
    name = CharField(max_length=50)
    model = CharField(max_length=50, null=True, unique=True)
    status = SmallIntegerField(default=DevilFruitStatus.NEW)
    owner = ForeignKeyField(User, null=True, backref='devil_fruit_owners', on_delete='RESTRICT', on_update='CASCADE')
    collection_date = DateTimeField(null=True)
    eaten_date = DateTimeField(null=True)
    expiration_date = DateTimeField(null=True)
    release_group_chat = ForeignKeyField(GroupChat, null=True, backref='devil_fruit_release_groups_chats',
                                         on_delete='RESTRICT', on_update='CASCADE')
    release_date = DateTimeField(null=True)
    release_message_id = IntegerField(null=True)
    should_show_abilities = BooleanField(default=False)

    class Meta:
        db_table = 'devil_fruit'

    def get_full_name(self) -> str:
        """
        Get fruit full name
        :return: Fruit full name
        """

        if self.model:
            return f"{self.name}, Model: {self.model}"
        else:
            return str(self.name)

    def get_status_description(self) -> str:
        """
        Get fruit status description
        :return: Fruit status description
        """

        return DevilFruitStatus(self.status).get_description()


DevilFruit.create_table()
