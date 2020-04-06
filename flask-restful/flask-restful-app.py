from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self, name):
        # next is like iterator.next(). This method use on collection
        item = next(filter(lambda x : x['name'] == name, items))
        return {'item': item}, 200 if item else 404 # return 200 and json item if found
        
        #return {'msg': 'Item not found'}, 404 # 404 is the http code that you want python to see.

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'msg': "An item with name '{}' already exists.".format(name)}, 400

        data = request.get_json()
        #data = request.get_json(force=True) # ignore content-type in header, it always converted to json
        #data = request.get_json(silent=True) # do not throw error when parsing failed. Just display empty page.
        item = {'name' : name, 'price': data['price']}
        items.append(item)
        return item, 201 # 201 - Created Successful, 202 - Create request accepted. (Migth not be created immediatly)

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

# app.run(port=5000)
app.run(port=5000, debug=True) # For display error page for debugging