import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db


app = Flask(__name__)

# in order to know when an object had changed
# but not been saved to the database,
# the extension flask SQLAlchemy
# was tracking every change that we made
# to the SQLAlchemy session,
# and that took some resources.
# Now we're turning it off because
# SQLAlchemy itself, the main library,
# has its own modification tracker
# which is a bit better.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turn-off tracker to increase performance because there is a tracker already in SQLALCHEMY core
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # read environment. If not found, use sqlite.
app.secret_key = 'jose'

api = Api(app)

# make flask SQLAlchemy automatically create db on first touching on models
# the created table will based on configuration in models
@app.before_request
def create_table():
    db.create_all()


jwt = JWT(app, authenticate, identity)

items = []

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':    
    db.init_app(app)    # This line will not run in uwsgi. Because __name__ will not be __main__ in uwsgi.
                        # Uwsgi will get app variable directly to run.
    app.run(port=5000, debug=True)