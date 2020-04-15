from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity
)
from models.user import UserModel

_user_parser_ = reqparse.RequestParser()
_user_parser_.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
_user_parser_.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

class UserRegister(Resource):

    def post(self):
        data = _user_parser_.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'msg': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'msg': 'User not found'}, 404
        user.delete_from_db()
        return {'msg': 'User deleted'}, 200

class UserLogin(Resource):
     
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser_.parse_args()

        # find user in databse
        user = UserModel.find_by_username(data['username'])

        # check password
        # This is what the 'authenticate()' function used to do.
        if user and safe_str_cmp(user.password, data['password']):
            # create access token
            # identity= is what the 'identity()' function used to do
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token (we will look at this later!)           
            refresh_token = create_refresh_token(user.id)
             # return them
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'msg': 'Invalid credentials'}, 401

        
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def get(self):       
        current_user = get_jwt_identity() 
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200