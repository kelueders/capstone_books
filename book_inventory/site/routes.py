from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from book_inventory.forms import BookForm
from book_inventory.models import Book, db

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
            author_first = bookform.author_first.data
            author_last = bookform.author_last.data
            summary = bookform.summary.data
            price = bookform.price.data
            num_pages = bookform.num_pages.data
            publisher = bookform.publisher.data
            published_year = bookform.publisher.data
            isbn = bookform.isbn.data
            user_token = current_user.token

            book = Book(title, author_first, author_last, summary, price,
                        num_pages, publisher, published_year, isbn, user_token)

            db.session.add(book)
            db.session.commit()

            return redirect(url_for('site.profile'))
        
    except:
        raise Exception('Book not created. Please check your form and try again.')
    
    user_token = current_user.token
    books = Book.query.filter_by(user_token = user_token)

    return render_template('profile.html', form = bookform, books = books)

