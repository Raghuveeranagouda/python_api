import sqlite3
from flask_restful import Resource, reqparse
from flask import request

class User:
    def __init__(self, _id, username, passowrd):
        self.id = _id
        self.username = username
        self.password = passowrd

    @classmethod
    def filter_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(select_query, (username,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user

    @classmethod
    def filter_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(select_query, (_id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user

class  UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Username is required!!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Password is required!!"
    )
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if User.filter_by_username(data['username']):
            return {'meassge': "User '{}' is already exist, please try with another username.".format(data['username'])}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        
        query = "INSERT INTO users VALUES(NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': "User created successfully."}, 201