from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#every class in restapi must inherit from Resource
class Item(Resource):

    #add a parser to go through the request data.
    #you can parse json as well as forms
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )
    #using a parser means that you cannot add any data that is not already defined in the 

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404  

    def post(self, name):
        #check if item is already in db
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name {name} already exists."}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data) #wherein **data is the same as data['price'], data['store_id']
        
        #abstracting the code in insert into a separate method allows us to run a try except on it so any errors in the operation
        #of the database can be caught
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500 #internal server error
        
        return item.json(), 201
        #code 200 is OK, some data was returned
        #code 201 is that some item is created
        #code 400 is bad request, user fault
        #code 500 is internal server error, not user fault

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}

    #put method can be used to create or update, and it will NOT create new items if same name already exists
    #it is idempotent (an operation that can be applied multiple times without changing the result beyond the initial application)

    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])

        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}