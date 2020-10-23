from models.user import UserModel
from werkzeug.security import safe_str_cmp #function can be used to compare strings

#a user accessing the auth endpoint sends their user and pw here which are passed into the function
def authenticate(username, password):
    #dictionary.get() method is like dict['key'], except you can add a default value should the key not exist
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

#payload is the content of the Jwt 
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)