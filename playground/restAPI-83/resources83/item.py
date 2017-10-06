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
        item =ItemModel(name,  data['price']) # an Object

        try:
            item.insert() #= self.insert(item), now obj function insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201 #201 is created, 202 accepted

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    # @jwt_required()
    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # updated_item = {'name': name, 'price': data['price']} # dict
        updated_item =ItemModel(name, data['price'])  #Obj

        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item."},500
        else:
            try:
                updated_item.update()
            except:
                raise
                return {"message": "An error occurred updating the item."},500
        return updated_item.json()

class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()

        return {'items': items}

