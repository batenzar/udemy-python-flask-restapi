from flask import Flask
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
        item = {'name' : name, 'price': 12.00}
        items.append(item)
        return item, 201 # 201 - Created Successful, 202 - Create request accepted. (Migth not be created immediatly)

api.add_resource(Item, '/item/<string:name>')

app.run(port=5000)