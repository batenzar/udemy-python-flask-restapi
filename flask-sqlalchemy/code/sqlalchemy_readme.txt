SQLAlchemy
- SQLAlchemy is an Object-Relational Mapping. It just map row from database to object automatically. 
It don't own storage. All data go to the relation database. (sqlite in this case)
- It automatically convert row to object if it can.
- Does not include in flask. You must install by 'pip install flask-sqlalchemy'
- In order to use SQLAlchemy, make sure that the tables in database 
are match with definition in models.user.py and models.item.py
