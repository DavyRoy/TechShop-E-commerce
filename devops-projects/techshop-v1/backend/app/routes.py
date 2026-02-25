from flask import Blueprint, jsonify, request
from app.models import Product, Category, Order, OrderItem
from app import db
import math

# Blueprint
api = Blueprint('api', __name__, url_prefix='/api')

# ============= GET ENDPOINTS =============

@api.route('/health')
def health():
    return jsonify({'status': 'ok'})

@api.route('/categories')
def get_categories():
    # Получить все категории из БД
    categories = Category.query.all()
    # Преобразовать в JSON
    categories_list = [category.to_dict() for category in categories]
    # Вернуть
    return jsonify(categories_list)

@api.route('/products')
def get_products():
    # Получить параметры page и limit
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    offset = (page - 1) * limit
    # Сделать запрос с pagination
    products = Product.query.offset(offset).limit(limit).all()
    # Посчитать total и pages
    total = Product.query.count()
    pages = math.ceil(total / limit)
    # Вернуть JSON
    return jsonify({
        'products': [product.to_dict() for product in products],
        'total': total,
        'pages': pages,
        'page': page,
        'limit': limit
    })

@api.route('/products/<int:product_id>')
def get_product(product_id):
    # Найти товар по ID
    product = Product.query.get(product_id)
    # Если не найден → 404
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    # Вернуть JSON
    return jsonify(product.to_dict())

@api.route('/products/category/<int:category_id>')
def get_products_by_category(category_id):
    # Найти товары по category_id
    products = Product.query.filter_by(category_id=category_id).all()
    # Вернуть JSON
    return jsonify([product.to_dict() for product in products])

# ============= POST ENDPOINTS =============

@api.route('/orders', methods=['POST'])
def create_order():
    # Получить JSON
    data = request.get_json()
    # Валидировать
    if not data:
        return jsonify({'error': "No data provided"}), 400
    # Посчитать total_price
    if 'customer_name' not in data or not data['customer_name']:
        return jsonify({'error': 'customer_name is required'}), 400
    if 'customer_email' not in data or not data['customer_email']:
        return jsonify({'error': 'customer_email is required'}), 400
    if '@' not in data['customer_email']:
        return jsonify({'error': 'Invalid email format'}), 400
    if 'items' not in data or not data['items']:
        return jsonify({'error': 'items is required'}), 400
    
    for item in data['items']:
        if 'product_id' not in item:
            return jsonify({'error': 'product_id is required in items'}), 400
        if 'quantity' not in item:
            return jsonify({'error': 'quantity is required in items'}), 400
        if item['quantity'] <= 0:
            return jsonify({'error': 'quantity must be > 0'}), 400
    # Создать Order и OrderItems
    try:
        total_price = 0
        for item in data['items']:
            product = Product.query.get(item['product_id'])
            if not product:
                return jsonify({"error": f"Product {item['product_id']} not found"}), 404
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
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=item['quantity'],
                price=product.price
            )
            db.session.add(order_item)
        db.session.commit()
        return jsonify({
            "message": "Order created successfully",
            "order_id": new_order.id,
            "total_price": float(total_price)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500