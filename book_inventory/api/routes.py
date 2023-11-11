from flask import Blueprint, request, jsonify, redirect, render_template, abort, url_for
from flask_login import login_required, current_user
from book_inventory.helpers import token_required
from book_inventory.models import db, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix='/api')

# Create Book Endpoint
@api.route('/books', methods = ['GET'])
@login_required
def create_book():

    the_args = dict(request.args)

    title = the_args['name']
    author = the_args['author']

    book = Book(title, author, current_user.token)
    
    # add the book and commit it to the database

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)        # converting the book Object into a Python dictionary so it can be jsonified ?

    jsonify(response)

    return redirect(url_for('site.profile'))        # have to jsonify things you get from AND push to API request

#Read 1 Single Book Endpoint
# @api.route('/books/<id>', methods = ['GET'])
# @login_required
# def get_book(id):
#     if id:
#         book = Book.query.get(id)
#         response = book_schema.dump(book)
#         return jsonify(response)
#     else:
#         return jsonify({'message': 'ID is missing'}), 401
    

# Read all the books
# @api.route('/books', methods = ['GET'])
# @login_required
# def get_books(our_user):
#     token = our_user.token
#     books = Book.query.filter_by(user_token = token).all()
#     response = books_schema.dump(books)

#     return jsonify(response)

# Update 1 Book by ID
@api.route('/books/update/<id>', methods = ['GET', 'POST'])
@login_required
def update_book(id):
    book = Book.query.get(id)
    
    if request.method == 'POST':
        if book:
            db.session.commit()

            title = request.form['title']

            book = Book(id=id, title=title)

            db.session.add(book)
            db.session.commit()
            return redirect(url_for("site.profile"))
        return f"Book with id = {id} does not exist."
    
    return render_template('update_book.html', book = book)

    # book.title = request.json['title']
    # # book.author = request.json['author']
    # # book.user_token = our_user.token

    # db.session.commit()

    # response = book_schema.dump(book)

    # return jsonify(response)

# @api.route('/book_form/<id>')
# @login_required
# def book_form(id):

#     return render_template('update_book.html', id=id)

# @api.route('/books', methods = ['GET'])
# @login_required
# def update_book():

#     the_args = dict(request.args)

#     the_id = the_args['id']

#     # calling up a book with this specific ID
#     book = Book.query.get(the_id)

#     # resetting the book title and author to what the user entered
#     book.title = the_args['title']
#     # book.author = the_args['author']

#     # committing to the database
#     db.session.commit()

#     # converting book object into Python dictionary
#     response = book_schema.dump(book) 

#     # jsonifying the dictionary so you can get from and push to API request 
#     jsonify(response)

#     return redirect("/profile")


# Delete 1 Book by ID
@api.route('/books/<id>', methods = ['GET'])
@login_required
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        abort(404)
    db.session.delete(book)
    db.session.commit()

    # response = book_schema.dump(book)

    # return jsonify(response)

    return redirect(url_for("site.profile"))

# @api.route('/books', methods = ['GET'])
# @login_required
# def delete_book():

#     the_args = dict(request.args)

#     id = the_args['id']

#     book = Book.query.get(id)
#     db.session.delete(book)
#     db.session.commit()

#     response = book_schema.dump(book)

#     jsonify(response)

#     return redirect("/profile")