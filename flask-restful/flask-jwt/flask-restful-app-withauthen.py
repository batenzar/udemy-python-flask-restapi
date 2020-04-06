from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required # Step 1.1 - import JWT (pip install flask-jwt)
from security import authenticate,identity # Step 4.2 import security from security.py

app = Flask(__name__)
# Step 2
app.secret_key = 'jose' # decide secret_key for other client

api = Api(app)

# Step 3 
jwt = JWT(app, authenticate, identity) # this line automatically create '/auth'

# Step 4.1 
# Create security.py
# Create authenticate(username, password) function
# Create identity(payload) function

items = []

class Item(Resource):
    @jwt_required() # Step 5 - add decoration to http method for authen before calling method
    def get(self, name):
        item = next(filter(lambda x : x['name'] == name, items))
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'msg': "An item with name '{}' already exists.".format(name)}, 400

        data = request.get_json()
        item = {'name' : name, 'price': data['price']}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)