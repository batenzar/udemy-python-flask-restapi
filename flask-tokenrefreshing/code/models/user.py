from db import db

class UserModel(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80)) # limit the size to 80 character
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self) 
        db.session.commit()   

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id): # we changed from 'id' to '_id' because sometime python use id as special variable. So, we should avoid using it.
        return cls.query.filter_by(id=_id).first()
        
