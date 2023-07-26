from flask import Blueprint, request, jsonify
from book_inventory.helpers import token_required
from book_inventory.models import db, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix='/api')

# Create Book Endpoint
@api.route('/books', methods = ['POST'])
@token_required
def create_book(our_user):

    title = request.json['title']
    author = request.json['author']
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    book = Book(title, author, user_token)
    
    # add the book and commit it to the database

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)        # converting the book Object into a Python dictionary so it can be jsonified ?

    return jsonify(response)        # have to jsonify things you get from AND push to API request

#Read 1 Single Book Endpoint
@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_book(our_user, id):
    if id:
        book = Book.query.get(id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401
    

# Read all the books
@api.route('/books', methods = ['GET'])
@token_required
def get_books(our_user):
    token = our_user.token
    books = Book.query.filter_by(user_token = token).all()
    response = books_schema.dump(books)

    return jsonify(response)

# Update 1 Book by ID
@api.route('/books/<id>', methods = ['PUT'])
@token_required
def update_book(our_user, id):
    book = Book.query.get(id)

    book.title = request.json['title']
    book.author = request.json['author']
    book.user_token = our_user.token

    db.session.commit()

    response = book_schema.dump(book)

    return jsonify(response)


#Delete 1 Book by ID
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(our_user, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    response = book_schema.dump(book)

    return jsonify(response)