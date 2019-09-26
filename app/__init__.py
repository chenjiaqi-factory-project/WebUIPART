from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
bootstrap = Bootstrap(app)

# blueprint for auth part
from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

# blueprint for elec part
from app.elec import bp as elec_bp
app.register_blueprint(elec_bp, url_prefix='/elec')

from app import routes
