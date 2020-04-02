from flask import Flask, jsonify, request

# Flask - a framework for web application which provided REST functionality
# jsonify - convert dictionary to json
# request - manage incoming request, getting data from request

app = Flask(__name__)

# Not A JSON. This is a list of map
stores = [
    {
        'name': 'My wonderful store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]

# POST /store data: {name: }
# Insert new store
@app.route('/store', methods=['POST'])
def create_store():
    # 1. pop data from request
    # 2. create dict of store
    # 3. append new dict to existing dict
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)

    # Jsonify parameter is a dictionary.
    # The new_store is already a dictionary. 
    # We don't need to wrap it into a dictionary
    return jsonify(new_store) 

# GET /store/<name>
# Return specific store
# Ex. http://127.0.0.1:5000/store/some_name
@app.route('/store/<string:name>') 
def get_store(name): # parameter matched with the route
    # 1. Iterate over stores
    # 2.1 If the store name matches, return it
    # 2.2 If  none match, return an error message
    for s in stores:
        if s['name'] == name:
            return jsonify(s)
    
    return jsonify({'message': 'store not found'})

# GET /store/
# Return all store
# response store as JSON (application/json)
#
# Result JSON
# {
#   "stores": [
#     {
#       "items": [
#         {
#           "name": "My Item",
#           "price": 15.99
#         }
#       ],
#       "name": "My wonderful store"
#     }
#   ]
# }
@app.route('/store') 
def get_stores():
    # stores is a list (not a dictionary). 
    # We need to wrap into dict before sending it to jsonify
    return jsonify({'stores':stores})

# POST /store/<string:name>/item
# Insert an item to store
@app.route('/store/<string:name>/item', methods=['POST']) 
def create_item_in_store(name):
    # 1. Iterate over stores
    # 2.1 If the store name matches, do create item.
    # 2.1.1 pop data from request, 
    # 2.1.2 create item dict, 
    # 2.1.3 append the created dict to existing store
    # 2.2 If  none match, return an error message
    for s in stores:
        if s['name'] == name:
            request_data = request.get_json()
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            s['items'].append(new_item)
            return jsonify(new_item) 

    return jsonify({'message': 'store not found'})

# GET /store/<string:name>/item
# Return items in store
@app.route('/store/<string:name>/item') 
def get_items_in_store(name):
    # 1. Iterate over stores
    # 2.1 If the store name matches, return its items
    # 2.2 If  none match, return an error message
    for s in stores:
        if s['name'] == name:
            return jsonify({'items':s['items']})

    return jsonify({'message': 'store not found'})

# -------------------------------
app.run(port=5000)    # start web server