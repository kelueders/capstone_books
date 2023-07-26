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
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    book = db.relationship('Book', backref = 'owner', lazy = True)

    def __init__(self, email, username, password):     
        self.id = self.set_id()
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
    author = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    # One User to Many Books, so the foreign key is in the Book Class

    def __init__(self, title, author, user_token):
        self.id = self.set_id()
        self.title = title
        self.author = author
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"'{self.title}' has been added to the database. Happy reading!"

class BookSchema(ma.Schema):
    class Meta:
        # these fields will come back from the API call
        fields = ['id', 'title', 'author']
        
book_schema = BookSchema()
books_schema = BookSchema(many = True)   # will bring back a list of objects