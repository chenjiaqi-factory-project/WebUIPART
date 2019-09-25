from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

# blueprint for water part
from app.elec import bp as elec_bp
app.register_blueprint(elec_bp, url_prefix='/elec')

from app import routes
