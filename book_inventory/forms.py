from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    first_name = StringField('first_name')
    last_name = StringField('last_name')
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])
    submit_button = SubmitField()

class BookForm(FlaskForm):
    title = StringField('title', validators = [DataRequired()])
    author_first = StringField('author_first', validators = [DataRequired()])
    author_last = StringField('author_last', validators = [DataRequired()])
    summary = StringField('summary')
    price = DecimalField('price', places=2)
    num_pages = IntegerField('num_pages', validators = [DataRequired()])
    publisher = StringField('publisher')
    published_year = StringField('published_year')
    isbn = StringField('isbn')
    submit_button = SubmitField()