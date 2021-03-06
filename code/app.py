from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from item import Item, Items

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)
app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
