from peewee import *
from app.models import DATABASE
from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash


class School(Model):
    """Model representing a School

    Each school has a unique id and name
    """

    school_id = PrimaryKeyField(db_column='ID')
    name = CharField(db_column='NAME', unique=True)

    @classmethod
    @DATABASE.transaction()
    def create_school(cls, name):
        """Class method to create a school with default permissions

        `name`: name of the school to be created
        """
        try:
            school = School.create(name=name)
        except IntegrityError:
            raise ValueError("Name is use.")

        # TODO: Remove unused permissions
        Permission.create(name='lecture_admin', description="Can create lectures", school=school.school_id)
        Permission.create(name='discussion_admin', description="Can create discussions", school=school.school_id)
        Permission.create(name='super_user', description="Is a superuser", school=school.school_id)
        Permission.create(name='lesson_admin', description="Can create lessons", school=school.school_id)
        Permission.create(name='note_admin', description="Can upload notes with non default semester", school=school.school_id)

    class Meta:
        database = DATABASE
        db_table = 'TBL_SCHOOL'


class User(UserMixin, Model):
    """Model representing a user

    Each user belongs to a school, represented with a int corresponding to a School.
    They have a unique email and id. They also have first and last names and a
    password that should be hashed using bcrypt. The UserMixin mixin makes the model
    compatible with the flask-login package. And inherits from the Model object to make use
    of the Peewee ORM.
    """
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
        """
        Creates a new user with a hashed password

        `email`: the email for the user to be created that must be unique and have the .edu top level domain.
        `password`: the unhashed password
        `school_id`: the school_id attribute of the School object the user is attending
        `first_name`: the user's first name
        `last_name`: the user's last name
        """

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
        """Returns user_id as a string for use with flask-login"""
        return str(self.user_id)

    def update_password(self, password):
        """Update user's password

        Takes in a raw password and automatically hashes it using and updates the user

        `password`: the user's new unhashed password
        """
        try:
            self.password = generate_password_hash(password)
            self.save()
        except Exception as e:
            raise e

    def has_permission(self, name):
        """Check whether a user has a permission with a given name

        `name`: the name of permission to check the user has

        """
        try:
            permission = Permission.get(Permission.name == name, Permission.school == self.school_id)
        except DoesNotExist:
            raise ValueError("Name does not exist.")

        try:
            user_permission = UserPermission.get(UserPermission.user == self.user_id,
                                                 UserPermission.permission == permission.id)
            return True
        except DoesNotExist:
            return False

    def has_any_permission(self, names):
        """Checks whether the user has any of the permission with a name in the list of names

        :param names: a list of names of permissions
        :type names: list
        """
        query = Permission.select().where((Permission.name << names) & (Permission.school == self.school_id))
        if not query.exists():
            raise ValueError("No valid permission names")
        ids = [p.id for p in query]
        if UserPermission.select().where((UserPermission.user == self.user_id) & (UserPermission.permission << ids)).exists():
            return True
        return False


class Permission(Model):
    """Model representing a permission that may be given to a user."""
    id = PrimaryKeyField(db_column='ID')
    school = ForeignKeyField(School, db_column='SCHOOL_ID')
    name = CharField(db_column='NAME')
    description = CharField(db_column='DESCRIPTION')

    class Meta:
        database = DATABASE
        db_table = 'TBL_PERMISSION'
        indexes = (
            (('name', 'school'), True),
        )


class UserPermission(Model):
    """Model representing a user having a permission"""
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER')
    permission = ForeignKeyField(Permission, db_column='PERMISSION')

    class Meta:
        database = DATABASE
        db_table = 'TBL_USER_PERMISSION'
        indexes = (
            (('user', 'permission'), True),
        )
