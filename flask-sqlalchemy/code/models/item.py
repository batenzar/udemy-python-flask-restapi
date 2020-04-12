from db import db

class ItemModel(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80)) # limit the size to 80 character
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel') # which store that item are in (1..*)

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price':self.price, 'store_id': self.store_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # "SELECT * FROM items WHERE name=? LIMIT 1"        

    def save_to_db(self):
        db.session.add(self) 
        db.session.commit()       

    def delete_from_db(self):
        db.session.delete(self) 
        db.session.commit()      

    # we don't need this method.
    # Uses save_to_db instead to update database
    # def update(self):