from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import Config
from prometheus_flask_exporter import PrometheusMetrics

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    from app.routes import api
    app.register_blueprint(api)
    metrics = PrometheusMetrics(app)

    return app
