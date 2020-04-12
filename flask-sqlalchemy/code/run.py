from app import flask-restful-app-withauthen
from db import db

db.init_app(app)

# make flask SQLAlchemy automatically create db on first touching on models
# the created table will based on configuration in models
@app.before_request
def create_table():
    db.create_all()
