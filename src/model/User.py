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
    join_date = DateTimeField(default=datetime.datetime.now)
    bounty = BigIntegerField(default=0)
    total_gained_bounty = BigIntegerField(default=0, constraints=[Check('total_gained_bounty >= 0')])
    pending_bounty = BigIntegerField(default=0)
    doc_q_cooldown_end_date = DateTimeField(null=True)
    game_cooldown_end_date = DateTimeField(null=True)
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
    last_system_interaction_date = DateTimeField(null=True)
    private_screen_list = CharField(max_length=99)
    private_screen_step = SmallIntegerField()
    private_screen_in_edit_id = IntegerField(null=True)
    bounty_gift_tax = IntegerField(default=0)
    is_admin = BooleanField(default=False)
    devil_fruit_collection_cooldown_end_date = DateTimeField(null=True)
    bounty_message_limit = BigIntegerField(default=0)
    timezone = CharField(max_length=99, null=True)
    is_active = BooleanField(default=True)
    prediction_creation_cooldown_end_date = DateTimeField(null=True)

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

    def get_display_name(self, add_user_id: bool = False) -> str:
        """
        Gets the user display name
        :param add_user_id: Add user id
        :return: User display name
        """
        return "{}{}{}{}".format(self.tg_first_name,
                                 " " + self.tg_last_name if self.tg_last_name is not None else "",
                                 " (@" + self.tg_username + ")" if self.tg_username is not None else "",
                                 " - " + self.tg_user_id if add_user_id else "")

    @staticmethod
    def get_by_string_filter(filter_by: str) -> list['User']:
        """
        Gets users by string filter, searching by first name, last name, username or user id
        :param filter_by: Filter by
        :return: Users
        """

        return User.select().where((User.tg_first_name.contains(filter_by)) |
                                   (User.tg_last_name.contains(filter_by)) |
                                   (User.tg_username.contains(filter_by)) |
                                   (User.tg_user_id.contains(filter_by))
                                   ).order_by(User.tg_first_name.desc()).limit(10)

    def is_warlord(self) -> bool:
        """
        Returns True if the user is a Warlord
        :return: True if the user is a Warlord
        """
        from src.model.Warlord import Warlord

        return self.warlords.where(Warlord.end_date > datetime.datetime.now()).count() > 0


User.create_table()
