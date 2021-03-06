from flask import Flask, request
from flask_restful import Resource, Api, reqparse
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
    # declare parser as static variable of Item class
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True, 
        help="This field cannot be left blank!"
    )

    @jwt_required() # Step 5 - add decoration to http method for authen before calling method
    def get(self, name):
        item = next(filter(lambda x : x['name'] == name, items))
        return {'item': item}, 200 if item else 404

    # create only. if exists, throw error
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'msg': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name' : name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        # don't forgot about variable scope
        # don't name this variable as 'items' it will shadowing the outer variable!!
        # use must declard 'global items' first to ensure that it will use outer variable
        items = list(filter(lambda x: x['name'] != name, items))
        return {'msg': 'Item deleted'}

    # update or create
    def put(self, name):
        data = Item.parser.parse_args() # replace 'data = request.get_json()'

        # If you try to print arugment that not defined, reqparse will throw KeyError
        # Even though it is in the JSON payload
        # print(data['anotherfield'])

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            # insert
            item = {'name':name,'price':data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)