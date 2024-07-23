from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False) 

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default='AVAILABLE')
    borrower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    borrower = db.relationship('User', backref='borrowed_books')
