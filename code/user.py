from os import curdir, name
import sqlite3
from sqlite3.dbapi2 import Connection, connect
from flask_restful import Resource, reqparse

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_name(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None        
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None        
        connection.close()
        return user


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="O campo username não pode ser em branco"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        nullable=True,
        help="O campo password não pode ser em branco"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        
        if User.find_by_name(data['username']):
            return {"message": "Usuario já existe"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "Usuario criado com sucesso"}, 201

