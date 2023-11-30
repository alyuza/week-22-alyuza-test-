import os
from flask import Flask
from flask_jwt_extended import JWTManager
from db import db
from common.bcrypt import bcrypt
from auth.apis import auth_blueprint
from user.apis import user_blueprint

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")

jwt = JWTManager(app)
db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(user_blueprint, url_prefix="/user")

# with app.app_context():
#     db_init()