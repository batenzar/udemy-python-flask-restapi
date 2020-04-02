from flask import Flask

app = Flask(__name__)

store = [
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
    # TODO
    pass

# GET /store/<name>
# Return specific store
# Ex. http://127.0.0.1:5000/store/some_name
@app.route('/store/<string:name>') 
def get_store(name): # parameter matched with the route
    pass

# GET /store/
# Return all store
@app.route('/store') 
def get_stores():
    pass

# POST /store/<string:name>/item
# Insert an item to store
@app.route('/store/<string:name>/item', ) 
def create_item_in_store():
    pass

# GET /store/<string:name>/item
# Return items in store
@app.route('/store/<string:name>/item') 
def get_items_in_store():
    pass

app.run(port=5000)    