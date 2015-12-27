from app.auth.models import School, Permission, UserPermission, User

schools = School.select()

for school in schools:
    Permission.get_or_create(name='lecture_admin', description="Can create lectures", school=school.school_id)
    Permission.get_or_create(name='discussion_admin', description="Can create discussions", school=school.school_id)
    su, created = Permission.get_or_create(name='super_user', description="Is a superuser", school=school.school_id)
    Permission.get_or_create(name='lesson_admin', description="Can crate lessons", school=school.school_id)

    has_superuser = False

    if UserPermission.select().where(UserPermission.permission == su.id).exists():
        has_superuser = True

    if not has_superuser:
        try:
            u = User.get(User.school_id == school.school_id)
            UserPermission.create(user=u.user_id, permission=su.id)
        except:
            pass