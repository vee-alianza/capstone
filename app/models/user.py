from .order import Order
from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(150))
    city = db.Column(db.String(150))
    state = db.Column(db.String(150))
    zip_code = db.Column(db.Integer)
    country = db.Column(db.String(150))


    orders = db.relationship('Order', backref='user', cascade='all, delete', lazy='dynamic')
    reviews = db.relationship('Review', backref='user', cascade='all, delete')
    cart = db.relationship('Cart_Item', backref='user', cascade='all, delete')

    @property
    def password(self):
        return self.hashed_password

    @property
    def pending(self):
        return self.orders.filter(Order.status == 'Pending').first()

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
