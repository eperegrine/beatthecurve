from flask import g, flash, redirect, url_for
from functools import wraps
from .models import Permission, UserPermission


def permission_required(name):
    """Decorator to wrap view functions to restrict their access to users with a given permissions

    `name`: The name of the permission required

    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if g.user.has_permission(name):
                return view_func(*args, **kwargs)
            flash("You are not authorised to access that page.")
            return redirect(url_for("auth_bp.profile"))
        return wrapper
    return decorator


def either_permission_required(names):
    """Decorator to wrap view functions to restrict their access to users which have any one of a list of permissions

    `names`: list of permission names which a user is required to have at least one of.

    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if g.user.has_any_permission(names):
                return view_func(*args, **kwargs)
            flash("You are not authorised to access that page.")
            return redirect(url_for("auth_bp.profile"))
        return wrapper
    return decorator