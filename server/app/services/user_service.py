from app.models import User


def get_user_by_id(user_id):
    return User.query.get(user_id)


def update_user_fields(user, user_data):
    updatable_fields = ["name", "mail", "surname"]
    for field in updatable_fields:
        if field in user_data:
            setattr(user, field, user_data[field])
