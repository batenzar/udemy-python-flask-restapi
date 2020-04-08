## We have code to create db.
# So, we can run python from 'code/' folder now
# (Make sure to create_tables.py first to create data.db)
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate,identity
from user import UserRegister
from item import Item, ItemList


app = Flask(__name__)
app.secret_key = 'jose'

api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)