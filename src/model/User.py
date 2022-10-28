import datetime

from peewee import *

from src.model.BaseModel import BaseModel
from src.model.Crew import Crew


class User(BaseModel):
    """
    User class
    """
    id = PrimaryKeyField()
    tg_user_id = CharField(max_length=99, unique=True)
    tg_first_name = CharField(max_length=99)
    tg_last_name = CharField(max_length=99)
    tg_username = CharField(max_length=99)
    bounty = BigIntegerField(default=0)
    pending_bounty = BigIntegerField(default=0)
    can_play_doc_q = BooleanField(default=True)
    can_initiate_game = BooleanField(default=True)
    bounty_poster_limit = SmallIntegerField(default=0)
    location_level = SmallIntegerField(default=0)
    should_propose_new_world = BooleanField(default=True)
    can_change_region = BooleanField(default=True)
    fight_immunity_end_date = DateTimeField(null=True)
    fight_cooldown_end_date = DateTimeField(null=True)
    impel_down_release_date = DateTimeField(null=True)
    impel_down_is_permanent = BooleanField(default=False)
    crew = ForeignKeyField(Crew, backref='crew_members', null=True)
    crew_join_date = DateTimeField(null=True)
    crew_role = SmallIntegerField(null=True)
    can_create_crew = BooleanField(default=True)
    can_join_crew = BooleanField(default=True)
    last_message_date = DateTimeField(default=datetime.datetime.now)
    private_screen_list = CharField(max_length=99)
    private_screen_step = SmallIntegerField()
    private_screen_in_edit_id = IntegerField(null=True)

    class Meta:
        db_table = 'user'

    def get_bounty_formatted(self) -> str:
        """
        Returns a formatted string of the bounty
        :return: The formatted string e.g. 1,000,000
        """

        return '{0:,}'.format(self.bounty)

    def is_arrested(self):
        """
        Returns True if the user is arrested
        :return: True if the user is arrested
        """

        return ((self.impel_down_release_date is not None and self.impel_down_release_date > datetime.datetime.now())
                or self.impel_down_is_permanent)


User.create_table()
