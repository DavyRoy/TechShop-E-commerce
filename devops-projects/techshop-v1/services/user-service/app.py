from flask import Flask
from app.extensions import db
from app.routes import auth_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@localhost:5432/techshop"

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(port=5020, debug=True)