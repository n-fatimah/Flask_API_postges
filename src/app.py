import logging

from flask import Flask
from flask import current_app as app
from flask_cors import CORS
from flask_migrate import Migrate

from api import blueprint
from config import settings
from model.base import db

logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder="../static")
app.app_context().push()

logging.getLogger().setLevel(level=logging.INFO)
logging.basicConfig(level=logging.INFO)

app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["CORS_HEADERS"] = "Content-Type"

app.register_blueprint(blueprint, url_prefix="/api/v1")
db.init_app(app)
Migrate(app, db)

CORS(app, max_age=600)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
