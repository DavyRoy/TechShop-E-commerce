from app import create_app, db
from app.models import Product, Category

app = create_app()

with app.app_context():
    # Очистить данные
    db.session.query(Product).delete()
    db.session.query(Category).delete()
    db.session.commit()

    # Категории
    categories = [
        Category(name='Laptops'),
        Category(name='Phones'),
        Category(name='Headphones'),
        Category(name='Cameras'),
        Category(name='Gaming'),
        Category(name='Watches'),
        Category(name='Tablets'),
        Category(name='Printers'),
        Category(name='Monitors'),
    ]
    db.session.add_all(categories)
    db.session.commit()  # ← сначала коммитим категории, потом продукты

    # Продукты
    products = [
        Product(name='MacBook Pro 13"', description='Apple M1 chip, 8GB RAM, 256GB SSD', price=1299.99, stock=10, category_id=1),
        Product(name='iPhone 11', description='A13 Bionic chip, 4GB RAM, 64GB storage', price=699.99, stock=5, category_id=2),
        Product(name='Samsung Galaxy S20', description='Exynos 9820 chip, 8GB RAM, 128GB storage', price=899.99, stock=7, category_id=2),
        Product(name='Sony WH-1000XM4', description='Noise-canceling wireless headphones', price=349.99, stock=15, category_id=3),
        Product(name='Canon EOS R5', description='45MP full-frame mirrorless camera', price=3899.99, stock=3, category_id=4),
        Product(name='PlayStation 5', description='Next-gen gaming console with ultra-fast SSD', price=499.99, stock=20, category_id=5),
        Product(name='Apple Watch Series 6', description='GPS + Cellular, Blood Oxygen app', price=399.99, stock=8, category_id=6),
        Product(name='iPad Pro 11"', description='Apple M1 chip, 8GB RAM, 128GB storage', price=799.99, stock=12, category_id=7),
        Product(name='HP LaserJet Pro M404n', description='Monochrome laser printer with fast printing speed', price=299.99, stock=10, category_id=8),
        Product(name='Dell UltraSharp U2720Q', description='27-inch 4K monitor with USB-C connectivity', price=599.99, stock=5, category_id=9),
        Product(name='MacBook Air M1', description='Apple M1 chip, 8GB RAM, 512GB SSD', price=999.99, stock=8, category_id=1),
        Product(name='iPhone 13 Pro', description='A15 Bionic chip, 6GB RAM, 256GB storage', price=999.99, stock=10, category_id=2),
        Product(name='AirPods Pro', description='Active noise cancellation, wireless charging', price=249.99, stock=20, category_id=3),
        Product(name='Sony A7 III', description='24MP full-frame mirrorless camera', price=1999.99, stock=5, category_id=4),
        Product(name='Xbox Series X', description='Next-gen gaming console, 1TB SSD', price=499.99, stock=15, category_id=5),
        Product(name='Samsung Galaxy Watch 4', description='Health monitoring, GPS, LTE', price=249.99, stock=12, category_id=6),
        Product(name='Samsung Galaxy Tab S7', description='Snapdragon 865+, 6GB RAM, 128GB storage', price=649.99, stock=8, category_id=7),
        Product(name='Canon PIXMA G3020', description='Wireless all-in-one ink tank printer', price=199.99, stock=7, category_id=8),
        Product(name='LG UltraWide 34"', description='34-inch curved ultrawide monitor', price=799.99, stock=4, category_id=9),
        Product(name='Nintendo Switch OLED', description='OLED screen, 64GB storage', price=349.99, stock=18, category_id=5),
        Product(name='Google Pixel 6', description='Google Tensor chip, 8GB RAM, 128GB storage', price=599.99, stock=6, category_id=2),
    ]
    db.session.add_all(products)
    db.session.commit()

    print(f'Categories: {Category.query.count()}')
    print(f'Products: {Product.query.count()}')
    print('Seed completed!')