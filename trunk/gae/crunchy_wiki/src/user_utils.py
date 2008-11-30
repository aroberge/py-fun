

from google.appengine.api import users

editors = {
    'andre': 'andre@test.com'
}

def is_editor():
    if users.is_current_user_admin():
        return True

    user = users.get_current_user()
    if user is None:
        return False

    if user.nickname() in editors:
        return True
    return False