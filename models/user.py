import sqlite3
from db import db

class UserModel(db.Model):
    #creating a table name
    __tablename__ = 'users'

    #creating columns of a database using SQLAlchemy database object.
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(80)) #Column has strings of max 80 characters
    password = db.Column(db.String(80))
    #these column names must match the init method details

    def __init__(self, username, password):
        #id is automatically generated
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod #class methods allow us to create methods that can instantiate classes
    def find_by_username(cls, username):
        """
        This class method looks through the database for rows (users) whose usernames match
        the argument of the method. It then returns the row. If there is such a row, that means
        the user is verified and you can instantiate a user object.
        """
        return cls.query.filter_by(username=username).first() #where the former is the column name and the later is the argument

    @classmethod #class methods allow us to create methods that can instantiate classes
    def find_by_id(cls, _id):
        """
        Same as above but with IDs
        """
        return cls.query.filter_by(id=_id)