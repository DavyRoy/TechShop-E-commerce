from app.models import Category, Product, Order, OrderItem

def test_get_categories_empty(client):
    """Тест получения категорий когда БД пуста"""
    response = client.get('/api/categories')
    
    assert response.status_code == 200
    assert response.json == []

def test_get_products_with_data(client, db):
    """Тест получения товаров"""
    # Создать категорию
    category = Category(name='Electronics', description='Electronic devices')
    db.session.add(category)
    db.session.commit()
    
    # Создать товар
    product = Product(
        name='Laptop',
        description='Gaming laptop',
        price=1299.99,
        stock=10,
        category_id=category.id
    )
    db.session.add(product)
    db.session.commit()
    
    # Сделать запрос
    response = client.get('/api/products')
    
    # Проверки
    assert response.status_code == 200
    data = response.json
    assert data['total'] == 1
    assert data['products'][0]['name'] == 'Laptop' 

def test_get_products_pagination_simple(client, db):
    """Тест pagination для товаров"""

    # Создать несколько товаров
    product = Product(name='Product 1', description='Desc 1', price=10.0, stock=5, category_id=None)
    product = Product(name='Product 2', description='Desc 2', price=10.0, stock=5, category_id=None)
    product = Product(name='Product 3', description='Desc 3', price=10.0, stock=5, category_id=None)
    product = Product(name='Product 4', description='Desc 4', price=10.0, stock=5, category_id=None)
    db.session.add(product)
    db.session.commit()
    # Запросить первую страницу
    response = client.get('/api/products?page=1&limit=10')
    # Проверить что пришли правильные товары
    assert response.status_code == 200
    data = response.json
    assert data['total'] == 1
    assert data['products'][0]['name'] == 'Product 1'
    # Проверить что pagination работает (total, pages, limit)
    assert data['pages'] == 1
    assert data['limit'] == 10

def test_get_products_pagination(client, db):
    """Тест pagination для товаров"""
    # Создать несколько товаров
    for i in range(15):
        product = Product(name=f'Product {i+1}', description=f'Desc {i+1}', price=10.0, stock=5, category_id=None)
        db.session.add(product)
    db.session.commit()
    # Запросить первую страницу
    response = client.get('/api/products?page=1&limit=10')
    # Проверить что пришли правильные товары
    assert response.status_code == 200
    data = response.json
    assert data['total'] == 15
    assert len(data['products']) == 10
    assert data['products'][0]['name'] == 'Product 1'
    # Проверить что pagination работает (total, pages, limit)
    assert data['pages'] == 2
    assert data['limit'] == 10

def test_get_product_by_id_success(client, db):
    """Тест получения товара по ID"""
    # Создать товар
    product = Product(name='Test Product', description='Test Description', price=10.0, stock=5, category_id=None)
    db.session.add(product)
    db.session.commit()
    
    # Запросить по ID
    response = client.get(f'/api/products/{product.id}')
    assert response.status_code == 200
    data = response.json
    assert data['name'] == 'Test Product'
    assert data['description'] == 'Test Description'
    assert data['price'] == 10.0
    # Проверить что вернулся правильный товар
    assert data['id'] == product.id

def test_get_product_by_id_not_found(client):
    """Тест 404 для несуществующего товара"""
    response = client.get('/api/products/999')
    
    assert response.status_code == 404
    assert 'error' in response.json

def test_get_products_by_category(client, db):
    """Тест фильтрации товаров по категории"""
    # Создать категорию
    category1 = Category(name='Electronics', description='Electronic devices')
    category2 = Category(name='Books', description='Books and literature')
    db.session.add(category1)
    db.session.add(category2)
    db.session.commit()
    # Создать товары в этой категории
    product1 = Product(name='Laptop', description='Gaming laptop', price=1299.99, stock=10, category_id=category1.id)
    product2 = Product(name='Book', description='Fantasy book', price=9.99, stock=5, category_id=category2.id)
    db.session.add(product1)
    db.session.add(product2)
    db.session.commit()
    # Создать товары в другой категории
    product3 = Product(name='Phone', description='Smartphone', price=699.99, stock=20, category_id=category1.id)
    product4 = Product(name='Magazine', description='Science magazine', price=19.99, stock=10, category_id=category2.id)
    db.session.add(product3)
    db.session.add(product4)
    db.session.commit() 
    # Запросить товары первой категории
    response = client.get(f'/api/products/category/={category1.id}')
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert len(data) == 2
    
    # Проверить что пришли только товары этой категории
    for product in data:
        assert product['category_id'] == category1.id

def test_create_order_success(client, db):
    """Тест успешного создания заказа"""
    # Создать товары
    product1 = Product(name='Laptop', description='Gaming laptop', price=1299.99, stock=10, category_id=None)
    product2 = Product(name='Book', description='Fantasy book', price=9.99, stock=5, category_id=None)
    db.session.add(product1)
    db.session.add(product2)
    db.session.commit()
    # Отправить POST с данными заказа
    order_data = {
        "customer_name": "John Doe",
        "customer_email": "johndoe@example.com",
        "products": [
            {"product_id": product1.id, "quantity": 1},
            {"product_id": product2.id, "quantity": 2}
        ]
    }
    response = client.post('/api/orders', json=order_data)
    # Проверить что заказ создан
    assert response.status_code == 201
    data = response.json
    assert 'order_id' in data
    order_id = data['order_id']
    # Проверить что заказ сохранен в БД
    order = Order.query.get(order_id)
    assert order is not None
    assert order.customer_name == "John Doe"
    assert order.customer_email == "johndoe@example.com"
    # Проверить что товары заказа сохранены
    assert len(order.items) == 2
    # Проверить что количество товаров корректно
    item1 = next((item for item in order.items if item.product_id == product1.id), None)
    item2 = next((item for item in order.items if item.product_id == product2.id), None)
    assert item1.quantity == 1
    assert item2.quantity == 2

def test_create_order_duplicate(client, db):
    """Тест создания дубликата заказа"""
    # Создать товары
    product1 = Product(name='Laptop', description='Gaming laptop', price=1299.99, stock=10, category_id=None)
    db.session.add(product1)
    db.session.commit()
    
    # Отправить заказ с теми же данными дважды
    order_data = {
        "customer_name": "John Doe",
        "customer_email": "johndoe@example.com",
        "products": [
            {"product_id": product1.id, "quantity": 1}
        ]
    }
    
    response = client.post('/api/orders', json=order_data)
    # Проверить что заказ создан
    assert response.status_code == 201
    data = response.json
    assert 'order_id' in data

def test_create_order_missing_fields(client):
    """Тест валидации - отсутствуют поля"""
    response = client.post('/api/orders', json={})
    
    assert response.status_code == 400
    assert 'error' in response.json

def test_create_order_invalid_product(client, db):
    """Тест создания заказа с несуществующим товаром"""
    # Отправить заказ с product_id=999
    order_data = {
        "customer_name": "John Doe",
        "customer_email": "johndoe@example.com",
        "products": [
            {"product_id": 999, "quantity": 1}
        ]
    }
    response = client.post('/api/orders', json=order_data)
    
    assert response.status_code == 400
    assert 'error' in response.json
       