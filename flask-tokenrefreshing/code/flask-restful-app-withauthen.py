from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from flask.json import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True # Flask will returns the specific error to match Exception. If we don't specific the code 500 always be returned.
app.secret_key = 'jose' # app.config['JWT_SECRET_KEY']
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    # Uses this method to check and add some property to token
    # The identity parameter is user_id in this case. (
    # The user_id is in the access_token created and returned from UserLogin.post())
    if identity == 1: # Hard-code for sample. In real scenario, we should read from some config file or database
        return {'is_admin': True}
    return {'is_admin':False}

# Tell flask-jwt-extended that when expired token has been sent to service
# what will be sent back to user
@jwt.expired_token_loader
def expired_token_callback(error):
    return jsonify({
        'msg': 'The token has expired', 
        'error': 'token_expired'
    }
    ),401

#@jwt.invalid_token_loader) # call when someone sent invalid jwt
#def invalid_token_loader_callback(error)

#@jwt.unauthorized_loader # call when someone sent invalid jwt
#def unauthorized_loader_callback(error)

#@jwt.needs_fresh_token_loader # call when someone call service which need fresh but token is not fresh
#def needs_fresh_token_loader_callback(error)

#@jwt.revoked_token_loader # call when token has been invoked (Ex. when logout)
#def revoked_token_loader_callback()


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
