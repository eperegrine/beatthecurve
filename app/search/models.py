from app.models import DATABASE
from peewee import *
from app.auth.models import User


class Option(Model):
    id = PrimaryKeyField(db_column='ID')
    description = CharField(db_column='DESCRIPTION')

    class Meta:
        database = DATABASE
        db_table = "TBL_OPTION"


class UserOption(Model):
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER_ID')
    option = ForeignKeyField(Option, db_column='OPTION_ID')

    class Meta:
        database = DATABASE
        db_table = "TBL_USER_OPTION"
