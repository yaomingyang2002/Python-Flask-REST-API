import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource): #define Resource
    parser = reqparse.RequestParser() # parser =>json
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    ) #here only define and accept 'price' as an arg of the parser!

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store_id."
    )

    @jwt_required()
    def get(self, name): #define method
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name): #exist
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        # item ={'name': name,  'price': data['price']} # a dict
        item =ItemModel(name,  data['price'], data['store_id']) # an Object

        try:
            item.save_to_db() #= self.insert(item), now obj function insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201 #201 is created, 202 accepted

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    # @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
