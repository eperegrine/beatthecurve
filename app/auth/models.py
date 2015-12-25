from peewee import *
from app.models import DATABASE
from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash


class School(Model):
    school_id = PrimaryKeyField(db_column='ID')
    name = CharField(db_column='NAME', unique=True)

    class Meta:
        database = DATABASE
        db_table = 'TBL_SCHOOL'


class User(UserMixin, Model):
    user_id = PrimaryKeyField(db_column='ID')
    email = CharField(db_column='EMAIL', unique=True)
    first_name = CharField(db_column='FIRST_NAME')
    last_name = CharField(db_column='LAST_NAME')
    password = CharField(db_column='PASSWORD')
    school_id = ForeignKeyField(School, db_column='SCHOOL_ID')
    karma_points = IntegerField(db_column='KARMA_POINTS', default=0)

    class Meta:
        database = DATABASE
        db_table = 'TBL_USER'

    @classmethod
    def create_user(cls, email, password, school_id, first_name, last_name):

        # Validate email
        if '@' not in email and email[-4:] is not '.edu':
            raise ValueError('Invalid Email')
        # Validate Password
        elif len(password) < 7:
            raise ValueError('Invalid Password')

        # Validate school_id
        try:
            school_id = int(school_id)
        except ValueError:
            raise TypeError("Invalid school_id type. Should be an int.")

        try:
            school = School.get(School.school_id == school_id)
        except DoesNotExist:
            raise ValueError('Invalid school_id')

        # Create user
        try:
            user = cls.create(
                email=email,
                password=generate_password_hash(password),
                school_id=school,
                first_name=first_name,
                last_name=last_name
            )
            return user
        except Exception as e:
            raise e

    def get_id(self):
        return str(self.user_id)

    def update_password(self, password):
        try:
            self.password = generate_password_hash(password)
            self.save()
        except Exception as e:
            raise e


class Permission(Model):
    id = PrimaryKeyField(db_column='ID')
    school = ForeignKeyField(School, db_column='SCHOOL_ID')
    name = CharField(db_column='NAME')
    description = CharField(db_column='DESCRIPTION')

    class Meta:
        database = DATABASE
        db_table = 'TBL_PERMISSION'


class UserPermission(Model):
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER')
    permission = ForeignKeyField(Permission, db_column='PERMISSION')

    class Meta:
        database = DATABASE
        db_table = 'TBL_USER_PERMISSION'
