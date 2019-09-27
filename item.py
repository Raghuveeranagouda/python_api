import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field can not be emapty!"
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': "Item not found!"}, 404
    
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.commit()
        connection.close()

        if row:
            return {'item':{'name':row[0], 'price':row[1]}}
        else:
            return None

    def post(self, name):

        if self.find_by_name(name):
            return {'message':"An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()
        try:
            item = self.add_item(name, data['price'])
        except:
            return {'message': "An error occured inserting the item"}, 500
        return item, 201

    @classmethod
    def add_item(cls, name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO items VALUES(?, ?)"
        result = cursor.execute(query, (name, price))
        connection.commit()
        connection.close()
        return {'item': {'name':name, 'price':price}}

    def delete(self, name):
        if not self.find_by_name(name):
            return {'message': "An item not exists!"}, 404
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "DELETE FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {'message': "Item Deleted"}

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name':name, 'price':data['price']}
        if item is None:
            item = self.add_item(name, data['price'])
            return {'message': "An item added"}

        else:
            try:
                self.update(updated_item)
                return {'message': "An item updated"}
            except:
                return {'message': "An error occurd while updating the item"}, 500

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        cursor.execute(query)
        items = cursor.fetchall()
        connection.close()
        return {'items': items}