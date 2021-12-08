from os import curdir
import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from flask import request


class Item(Resource):
    def parser_aqui():
        parser = reqparse.RequestParser()
        parser.add_argument(
            'price',
            type=float,
            required=True,
            help="Este campo não pode ser em branco"
        )
        return parser.parse_args()

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item não encontrado'}, 404


    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': "O item '{}' já existe".format(name)}, 400
        data = request.get_json()
        item = {'name': name, "price": data['price']}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'],item['price']))
        connection.commit()
        connection.close()
        
        return item, 201

    @jwt_required()
    def delete(self, name):
        if self.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            return {'message': 'Item deleted'}
        return {'message' : 'item não existe'}

    @jwt_required()
    def put(self, name):
        data = request.get_json()
        if self.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "UPDATE items SET price=? WHERE name=?"
            cursor.execute(query, (data['price'], name))
            connection.commit()
            connection.close()
            return {'message': 'Item atualizado'}
        else:
            return self.post(name)


class Items(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        # rows = result.fetchall()
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()
        return {'items': items}
        
