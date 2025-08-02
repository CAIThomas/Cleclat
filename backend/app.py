# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from models import db
from flask_migrate import Migrate
from routes.appartement import appartements_bp
from routes.users import users_bp


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# Enregistrer les blueprints avec des noms explicites
app.register_blueprint(appartements_bp, url_prefix='/appartements')
app.register_blueprint(users_bp, url_prefix='/users')
# app.register_blueprint(subscription_bp)  # À retirer si tu n'en as plus besoin

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

