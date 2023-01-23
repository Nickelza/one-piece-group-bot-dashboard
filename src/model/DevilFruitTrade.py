from peewee import *

from src.model.BaseModel import BaseModel
from src.model.DevilFruit import DevilFruit
from src.model.User import User


class DevilFruitTrade(BaseModel):
    """
    Devil Fruit Trade class
    """
    id = PrimaryKeyField()
    devil_fruit = ForeignKeyField(DevilFruit, backref='devil_fruit_trades', on_delete='RESTRICT', on_update='CASCADE')
    giver = ForeignKeyField(User, backref='devil_fruit_trade_givers', on_delete='RESTRICT', on_update='CASCADE')
    receiver = ForeignKeyField(User, backref='devil_fruit_trade_receivers', on_delete='RESTRICT', on_update='CASCADE')
    price = BigIntegerField(null=True)
    from_admin = BooleanField(default=False)
    from_bot = BooleanField(default=False)
    reason = CharField(max_length=100, null=True)
    date = DateTimeField()

    class Meta:
        db_table = 'devil_fruit_trade'


DevilFruitTrade.create_table()
