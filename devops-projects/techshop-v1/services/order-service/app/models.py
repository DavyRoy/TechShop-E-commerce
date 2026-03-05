import uuid
from datetime import datetime
from app import db


class Order(db.Model):
    __tablename__ = 'orders'

    id           = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id      = db.Column(db.String(36), nullable=False)
    status       = db.Column(db.String(50), nullable=False, default='pending')
    total_amount = db.Column(db.Float, nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow)
    items        = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id             = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id       = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    product_id     = db.Column(db.String(100), nullable=False)
    quantity       = db.Column(db.Integer, nullable=False)
    price_snapshot = db.Column(db.Float, nullable=False)  # цена на момент заказа