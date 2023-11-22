import datetime

from peewee import *

from src.model.BaseModel import BaseModel
from src.model.User import User


class Warlord(BaseModel):
    """
    Warlord class
    """
    id = PrimaryKeyField()
    user = ForeignKeyField(User, backref='warlords', on_delete='CASCADE', on_update='CASCADE')
    epithet = CharField(max_length=99, null=True)
    reason = CharField(max_length=999, null=True)
    date = DateTimeField(default=datetime.datetime.now)
    end_date = DateTimeField()
    original_end_date = DateTimeField()  # In case it was ended early
    revoke_reason = CharField(max_length=999, null=True)

    class Meta:
        db_table = 'warlord'

    @staticmethod
    def get_active() -> list['Warlord']:
        """
        Get active warlords
        :return: Active warlords
        """

        return (Warlord
                .select()
                .where(Warlord.end_date > datetime.datetime.now()))

    @staticmethod
    def get_active_count() -> int:
        """
        Get active warlords count
        :return: Active warlords count
        """

        return len(Warlord.get_active())

    @staticmethod
    def get_active_order_by_bounty() -> list['Warlord']:
        """
        Get active warlords
        :return: Active warlords
        """

        return (Warlord
                .select()
                .join(User)
                .where(Warlord.end_date > datetime.datetime.now())
                .order_by(User.bounty.desc()))

    @staticmethod
    def get_active_user_ids() -> list[int]:
        """
        Get active warlords
        :return: Active warlords
        """

        return [warlord.user.id for warlord in Warlord.get_active()]

    @staticmethod
    def get_latest_active_by_user(user: User) -> 'Warlord':
        """
        Get the latest active warlord by user
        :param user: The user
        :return: The warlord
        """

        return (Warlord
                .select()
                .where((Warlord.user == user) & (Warlord.end_date > datetime.datetime.now()))
                .order_by(Warlord.end_date.desc())
                .first())

    def get_end_date_by_duration(self, duration_days: int) -> datetime:
        """
        Get end date by duration
        :param duration_days: Duration in days
        :return: End date
        """

        return self.date + datetime.timedelta(days=duration_days)

    @staticmethod
    def get_by_string_filter(filter_by: str, only_active: bool = True) -> list['Warlord']:
        """
        Gets warlords by string filter, searching by first name, last name, username, user id, epithet, reason
        :param filter_by: Filter by
        :param only_active: Only active
        :return: Warlords
        """

        query = (Warlord
                 .select()
                 .join(User)
                 .where((User.tg_first_name.contains(filter_by)) |
                        (User.tg_last_name.contains(filter_by)) |
                        (User.tg_username.contains(filter_by)) |
                        (User.tg_user_id.contains(filter_by)) |
                        (Warlord.epithet.contains(filter_by)) |
                        (Warlord.reason.contains(filter_by))
                        ).limit(10))

        if only_active:
            query = query.where(Warlord.end_date > datetime.datetime.now())

        return query.execute()

    @staticmethod
    def get_all(only_active: bool = True) -> list['Warlord']:
        """
        Gets all warlords
        :param only_active: Only active
        :return: Warlords
        """

        if only_active:
            return Warlord.get_active()

        return Warlord.select().order_by(Warlord.date.desc()).execute()

    def is_active(self) -> bool:
        """
        Returns True if the warlord is active
        :return: True if the warlord is active
        """

        return self.end_date > datetime.datetime.now()


Warlord.create_table()
