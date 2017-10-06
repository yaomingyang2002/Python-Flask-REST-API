from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, ItemList
from resources.user import UserRegister
from security import authenticate, identity
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #worked in all SQL DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turn off the tracking
app.secret_key = 'jose'
api = Api(app) #define API

@app.before_first_request
def create_tables():
    db.create_all() #will create those imported!

jwt = JWT(app, authenticate, identity) #auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':     #only run this file will do the following
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

