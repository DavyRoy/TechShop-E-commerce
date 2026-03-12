from flask import Blueprint, jsonify, request
from app.models import Product, Category, Order, OrderItem
from app import db
from app.cache import get_from_cache, set_to_cache, invalidate_cache, redis_client
import math

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/health')
def health():
    return jsonify({'status': 'ok'})

@api.route('/categories')
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])

@api.route('/products')
def get_products():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    offset = (page - 1) * limit
    cache_key = f'products:all:page:{page}'

    cached = get_from_cache(cache_key)
    if cached:
        return jsonify(cached)

    products = Product.query.offset(offset).limit(limit).all()
    total = Product.query.count()
    pages = math.ceil(total / limit)

    result = {
        'products': [p.to_dict() for p in products],
        'total': total,
        'pages': pages,
        'page': page,
        'limit': limit
    }

    set_to_cache(cache_key, result, ttl=300)
    return jsonify(result)

@api.route('/products/<int:product_id>')
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict())

@api.route('/products/category/<int:category_id>')
def get_products_by_category(category_id):
    products = Product.query.filter_by(category_id=category_id).all()
    return jsonify([p.to_dict() for p in products])

@api.route('/cache/stats')
def cache_stats():
    info = redis_client.info()
    return jsonify({
        'hits': info.get('keyspace_hits', 0),
        'misses': info.get('keyspace_misses', 0),
        'keys': redis_client.dbsize(),
        'memory': info.get('used_memory_human', '0B')
    })

@api.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    if not data.get('customer_name'):
        return jsonify({'error': 'customer_name is required'}), 400
    if not data.get('customer_email') or '@' not in data['customer_email']:
        return jsonify({'error': 'Valid customer_email is required'}), 400
    if not data.get('items'):
        return jsonify({'error': 'items is required'}), 400

    for item in data['items']:
        if 'product_id' not in item or 'quantity' not in item:
            return jsonify({'error': 'product_id and quantity required in items'}), 400
        if item['quantity'] <= 0:
            return jsonify({'error': 'quantity must be > 0'}), 400

    try:
        total_price = 0
        for item in data['items']:
            product = Product.query.get(item['product_id'])
            if not product:
                return jsonify({'error': f"Product {item['product_id']} not found"}), 404
            total_price += product.price * item['quantity']

        new_order = Order(
            user_name=data['customer_name'],
            user_email=data['customer_email'],
            total_price=total_price,
            status='pending'
        )
        db.session.add(new_order)
        db.session.flush()

        for item in data['items']:
            product = Product.query.get(item['product_id'])
            db.session.add(OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=item['quantity'],
                price=product.price
            ))

        db.session.commit()
        invalidate_cache('products:*')
        return jsonify({
            'message': 'Order created successfully',
            'order_id': new_order.id,
            'total_price': float(total_price)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500