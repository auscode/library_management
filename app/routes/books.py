from flask import Blueprint, request, jsonify
from app.models import Book, db,User
from app.utils import role_required
from flask_jwt_extended import get_jwt_identity

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['POST'])
@role_required('LIBRARIAN')
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully!'}), 201

@books_bp.route('/<int:id>', methods=['PUT'])
@role_required('LIBRARIAN')
def update_book(id):
    data = request.get_json()
    book = Book.query.get_or_404(id)
    book.title = data['title']
    book.author = data['author']
    db.session.commit()
    return jsonify({'message': 'Book updated successfully!'}), 200

@books_bp.route('/<int:id>', methods=['DELETE'])
@role_required('LIBRARIAN')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully!'}), 200

@books_bp.route('/view', methods=['GET'])
def view_books():
    print("view_books")
    books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'status': book.status} for book in books]), 200


@books_bp.route('/<int:id>/borrow', methods=['POST'])
@role_required('MEMBER')
def borrow_book(id):
    book = Book.query.get_or_404(id)
    user_identity = get_jwt_identity()
    user = User.query.filter_by(username=user_identity['username']).first_or_404()

    if book.status == 'BORROWED':
        return jsonify({'message': 'Book is already borrowed'}), 400
    if book.borrower_id is not None:
        return jsonify({'message': 'Book is already borrowed by someone else'}), 400
    
    book.status = 'BORROWED'
    book.borrower_id = user.id
    db.session.commit()
    return jsonify({'message': 'Book borrowed successfully!'}), 200

@books_bp.route('/<int:id>/return', methods=['POST'])
@role_required('MEMBER')
def return_book(id):
    book = Book.query.get_or_404(id)
    user_identity = get_jwt_identity()
    user = User.query.filter_by(username=user_identity['username']).first_or_404()

    if book.status == 'AVAILABLE':
        return jsonify({'message': 'Book is already available'}), 400
    if book.borrower_id != user.id:
        return jsonify({'message': 'You are not the one who borrowed this book'}), 403
    
    book.status = 'AVAILABLE'
    book.borrower_id = None
    db.session.commit()
    return jsonify({'message': 'Book returned successfully!'}), 200

# @books_bp.route('/<int:id>/borrow', methods=['POST'])
# @role_required('MEMBER')
# def borrow_book(id):
#     book = Book.query.get_or_404(id)
#     if book.status == 'BORROWED':
#           return jsonify({'message': 'Book is already borrowed'}), 400
#     book.status = 'BORROWED'
#     db.session.commit()
#     return jsonify({'message': 'Book borrowed successfully!'}), 200

# @books_bp.route('/<int:id>/return', methods=['POST'])
# @role_required('MEMBER')
# def return_book(id):
#     book = Book.query.get_or_404(id)
#     if book.status == 'AVAILABLE':
#         return jsonify({'message': 'Book is already available'}), 400
#     book.status = 'AVAILABLE'
#     db.session.commit()
#     return jsonify({'message': 'Book returned successfully!'}), 200