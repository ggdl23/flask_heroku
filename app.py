import os

from flask import Flask
from flask_restful import Api #resouce is an object APIs can return
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') #If database_url is absent as an environment var, use the 2nd argument
app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False #this turns off the flask sqlalchemy modification tracker, but not the main sqlalchemy one
#authentication
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request #this decorator makes its method run before the first request into this app
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) #this function creates a new endpoint /auth. When called, we send it username and pw. and the function sends it
# to the authenticate function in the security script

#this command allows the resource Student to be accessible via link in the second argument
#this command can be used in place of the decorator @app.route('/student/<string:name>')
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, '/register')
#here, each class and its methods(endpoints) are resources we can access as users

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)


#STEPS TO CREATE API:
#1. Create the resource that is getting called. This resource class will contain endpoints the user can access
#2. Run api.add_resouce and add that class, as well as the endpoint url ('/items')
#3. Additional class functionality like a request parser for put and post requests can be added to the class.
#4. Add your authorization methods