from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self, name):
        for i in items:
            if i['name'] == name:
                return i
        return {'msg': 'Item not found'}, 404 # 404 is the http code that you want python to see.

    def post(self, name):
        data = request.get_json()
        #data = request.get_json(force=True) # ignore content-type in header, it always converted to json
        #data = request.get_json(silent=True) # do not throw error when parsing failed. Just display empty page.
        item = {'name' : name, 'price': 12.00}
        items.append(item)
        return item, 201 # 201 - Created Successful, 202 - Create request accepted. (Migth not be created immediatly)

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

# app.run(port=5000)
app.run(port=5000, debug=True) # For display error page for debugging