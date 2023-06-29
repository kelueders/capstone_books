from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import UserMixin, LoginManager

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    # creating our table and all the columns and setting them to their particular types
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    book = db.relationship('Book', backref = 'owner', lazy = True)

    def __init__(self, email, username, password, first_name = '', last_name = ''):     
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
        self.username = username

    def set_id(self): 
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)
    
    def __repr__(self):
        return f"User {self.email} has been added to the database!"
    
class Book(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(150))
    author_first = db.Column(db.String(20))
    author_last = db.Column(db.String(30))
    summary = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision = 7, scale = 2))
    num_pages = db.Column(db.Integer)
    publisher = db.Column(db.String(100), nullable = True)
    published_year = db.Column(db.String(150), nullable = True)
    isbn = db.Column(db.String(30), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    # One User to Many Books, so the foreign key is in the Book Class

    def __init__(self, title, author_first, author_last, summary, price, num_pages, 
                 publisher, published_year, isbn, user_token):
        self.id = self.set_id()
        self.title = title
        self.author_first = author_first
        self.author_last = author_last
        self.summary = summary
        self.price = price
        self.num_pages = num_pages
        self.publisher = publisher
        self.published_year = published_year
        self.isbn = isbn
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"'{self.title}' has been added to the database. Happy reading!"

class BookSchema(ma.Schema):
    class Meta:
        # these fields will come back from the API call
        fields = ['id', 'title', 'author_first', 'author_last', 'summary', 'price', 'num_pages', 
                  'publisher', 'published_year', 'isbn']
        
book_schema = BookSchema()
books_schema = BookSchema(many = True)   # will bring back a list of objects