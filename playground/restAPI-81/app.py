from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, ItemList
from resources.user import UserRegister
from security import authenticate, identity

app = Flask(__name__)
# auto assign the:  __name__ == '__main__' only when run this file
app.secret_key = 'jose'
api = Api(app) #define API
jwt = JWT(app, authenticate, identity) #auth


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    #mean only run this file will do the following not when imported by other file
    app.run(port=5000, debug=True)

