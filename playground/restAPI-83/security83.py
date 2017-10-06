from werkzeug.security import safe_str_cmp  # safe-string-compare

from models.user import UserModel


# users = [   User(1, 'user1', 'abcxyz'), User(2, 'user2', 'abcxyz'), ]
# username_table = {u.username: u for u in users}
# userid_table = {u.id: u for u in users}

#instead store data in memory db now store and retrieve in sqlite3 db
def authenticate(username, password):
    # user = username_table.get(username, None)
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    # return userid_table.get(user_id, None)
    return UserModel.find_by_id(user_id)