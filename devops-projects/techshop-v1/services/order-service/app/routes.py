import os
import requests
from datetime import datetime
from flask import Blueprint, request, jsonify
from app import db
from app.models import Order, OrderItem
from app.kafka_producer import publish_order_created, publish_order_updated, publish_order_cancelled

orders_bp = Blueprint('orders', __name__)

PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://localhost:8080')

def error_response(code, message, status):
    return jsonify({'error': {'code': code, 'message': message, 'status': status}}), status

def get_product_price(product_id: str) -> float:
    url = f"{PRODUCT_SERVICE_URL}/products/{product_id}"
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise ValueError(f"Product {product_id} not found")
    return response.json()['data']['price']

@orders_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'order-service'}), 200

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data.get('user_id')
    items = data.get('items', [])

    if not user_id or not items:
        return error_response('VALIDATION_ERROR', 'user_id and items required', 400)

    total = 0
    order_items_data = []

    for item in items:
        try:
            price = get_product_price(item['product_id'])
        except ValueError as e:
            return error_response('PRODUCT_NOT_FOUND', str(e), 422)

        total += price * item['quantity']
        order_items_data.append({
            'product_id': item['product_id'],
            'quantity': item['quantity'],
            'price_snapshot': price
        })

    order = Order(user_id=user_id, total_amount=total)
    db.session.add(order)
    db.session.flush()  #

    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data['product_id'],
            quantity=item_data['quantity'],
            price_snapshot=item_data['price_snapshot']
        )
        db.session.add(order_item)

    db.session.commit()

    publish_order_created({
        'order_id': order.id,
        'user_id': order.user_id,
        'items': order_items_data,
        'total_amount': total,
        'status': 'pending',
        'timestamp': datetime.utcnow().isoformat()
    })

    return jsonify({'data': {'order_id': order.id, 'status': order.status, 'total_amount': total}}), 201

@orders_bp.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return error_response('ORDER_NOT_FOUND', 'Order not found', 404)
    return jsonify({'data': {'order_id': order.id, 'user_id': order.user_id, 'status': order.status, 'total_amount': order.total_amount}}), 200

@orders_bp.route('/orders', methods=['GET'])
def list_orders():
    user_id = request.args.get('user_id')
    orders = Order.query.filter_by(user_id=user_id).all() if user_id else Order.query.all()
    return jsonify({'data': [{'order_id': o.id, 'status': o.status, 'total_amount': o.total_amount} for o in orders]}), 200

@orders_bp.route('/orders/<order_id>/status', methods=['PUT'])
def update_status(order_id):
    order = Order.query.get(order_id)
    if not order:
        return error_response('ORDER_NOT_FOUND', 'Order not found', 404)

    data = request.get_json()
    new_status = data.get('status')

    order.status = new_status
    order.updated_at = datetime.utcnow()
    db.session.commit()

    publish_order_updated({'order_id': order.id, 'status': new_status, 'updated_at': order.updated_at.isoformat()})
    return jsonify({'data': {'order_id': order.id, 'status': order.status}}), 200

@orders_bp.route('/orders/<order_id>', methods=['DELETE'])
def cancel_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return error_response('ORDER_NOT_FOUND', 'Order not found', 404)

    if order.status in ['shipped', 'delivered']:
        return error_response('CANNOT_CANCEL', 'Cannot cancel order in current status', 422)

    order.status = 'cancelled'
    db.session.commit()

    publish_order_cancelled(order.id)
    return jsonify({'data': {'order_id': order.id, 'status': 'cancelled'}}), 200