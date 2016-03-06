from app.auth.models import *
from app.search.models import *
import sys

argv_length = len(sys.argv)
print(sys.argv)
print(argv_length)
if argv_length > 5:
    school_name = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    first_name = sys.argv[4]
    last_name = sys.argv[5]
elif argv_length > 4:
    school_name = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    first_name = sys.argv[4]
    last_name = 'user'
elif argv_length > 3:
    school_name = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    first_name = 'test'
    last_name = 'user'
elif argv_length > 2:
    school_name = sys.argv[1]
    email = sys.argv[2]
    password = 'password'
    first_name = 'test'
    last_name = 'user'
elif argv_length > 1:
    school_name = sys.argv[1]
    user_name = 'test.user@test.edu'
    password = 'password'
    first_name = 'test'
    last_name = 'user'
else:
    school_name = 'test_school'
    email = 'test.user@test.edu'
    password = 'password'
    first_name = 'test'
    last_name = 'user'


School.create_school(name=school_name)
school = School.get(School.name==school_name)

user = User.create_user(
    email=email,
    password=password,
    first_name=first_name,
    last_name=last_name,
    school_id=school.school_id
)

super_user_permission = Permission.get(
    Permission.school == school.school_id,
    Permission.name == 'super_user'
)

UserPermission.create(permission=super_user_permission, user=user)

