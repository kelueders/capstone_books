from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from book_inventory.forms import BookForm
from book_inventory.models import Book, db
import requests

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    print("Here is my project about books!")
    return render_template('index.html')

@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    bookform = BookForm()

    try:
        if request.method == 'POST' and bookform.validate_on_submit():
            title = bookform.title.data
            author = bookform.author.data
            user_token = current_user.token

            book = Book(title, author, user_token)

            db.session.add(book)
            db.session.commit()

            return redirect(url_for('site.profile'))
        
    except:
        raise Exception('Book not created. Please check your form and try again.')
    
    user_token = current_user.token
    books = Book.query.filter_by(user_token = user_token)

    return render_template('profile.html', form = bookform, books = books)

@site.route('/list')
@login_required
def list_by_genre():
    url = "https://hapi-books.p.rapidapi.com/week/romance/10"
    headers = {
        "X-RapidAPI-Key": '24242474c2msh279df8013b73b3ap1cf7b1jsncf839b04e2e2',
        "X-RapidAPI-Host": 'hapi-books.p.rapidapi.com'
    }

    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        data = response.json()
    else:
        data = {}
        print(f"Please check book ID and try again: {response.status_code}")

    return render_template('booklist.html', top_books = data)

