import pytest
import os
from app import create_app, db as _db
from app.models import Category, Product

@pytest.fixture(scope='session')
def app():
    """Создаёт Flask приложение для тестов"""
    # Установить переменные окружения
    os.environ['TESTING'] = 'True'
    os.environ['POSTGRES_USER'] = 'test'
    os.environ['POSTGRES_PASSWORD'] = 'test'
    os.environ['POSTGRES_HOST'] = 'localhost'
    os.environ['POSTGRES_PORT'] = '5432'  # ✅ Исправлено с 5433 на 5432
    os.environ['POSTGRES_DB'] = 'testdb'
    os.environ['SECRET_KEY'] = 'test-secret-key'
    
    app = create_app()
    app.config['TESTING'] = True
    
    # ✅ ВАЖНО: Переопределить DATABASE_URI напрямую для тестов
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test:test@localhost:5432/testdb'
    
    return app

@pytest.fixture(scope='session')
def client(app):
    """Создаёт test client"""
    return app.test_client()

@pytest.fixture(scope='function')
def db(app):
    """Создаёт и очищает БД для каждого теста"""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()
