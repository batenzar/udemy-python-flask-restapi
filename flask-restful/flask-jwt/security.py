
from werkzeug.security import safe_str_cmp # useful for fixing string comparison issue because of encoding, etc problem
from user import User

# All users
users = [
    User(1,'bob', 'asdf')
]

# user mapped by name. (just for faster access)
username_mapping = { u.username: u for u in users }

# user mapped by id. (just for faster access)
userid_mapping={ u.id: u for u in users }

def authenticate(username, password):
    user = username_mapping.get(username,None)
    if user and safe_str_cmp(user.password, password): # python 2.7 style
    # if user and user.password == password: # not safe for authenticate
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)