from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2)) #precision is number of numbers after the decimal points

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship("StoreModel")

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        #returns a json representation of the item
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        #returns an ItemModel object that corresponds to the entered name
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()

        # if row:
        #     return cls(*row)
        return cls.query.filter_by(name=name).first() #this method is inherited from db.Model object
        #The entire commenting block can be accomplished by this one line

    def save_to_db(self):
        #we add self which is an object, directly into the dataframe
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()