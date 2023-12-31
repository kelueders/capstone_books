from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
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
    # author = StringField('author', validators = [DataRequired()])
    submit_button = SubmitField()

class GenreForm(FlaskForm):
    genre = SelectField('genre', choices=[('romance', 'fantasy', 'mystery', 'horror', 'thriller')])
    submit_button = SubmitField()