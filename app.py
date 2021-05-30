from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from werkzeug.security import safe_str_cmp
from Resources.user import UserRegister
from Resources.item import Item
from Resources.item import ItemList

################################

app=Flask(__name__)
app.secret_key='sona'
api=Api(app)

jwt=JWT(app,authenticate,identity) #/auth

    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')

if __name__=='__main__':
    app.run(port=5000,debug=True)

