from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2)) #precision is number of numbers after the decimal points

    items = db.relationship("ItemModel", lazy="dynamic") #lazy dyamic causes self.items to no longer raise a list of items but is now a query builder

    def __init__(self, name):
        self.name = name

    def json(self):
        #returns a json representation of the item
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #this method is inherited from db.Model object
        #The entire commenting block can be accomplished by this one line

    def save_to_db(self):
        #we add self which is an object, directly into the dataframe
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()