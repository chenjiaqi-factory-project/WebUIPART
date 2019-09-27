from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
bootstrap = Bootstrap(app)

login.login_view = 'auth.login_view'

# blueprint for auth part
from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

# blueprint for elec part
from app.elec import bp as elec_bp
app.register_blueprint(elec_bp, url_prefix='/elec')

# blueprint for gas part
from app.gas import bp as gas_bp
app.register_blueprint(gas_bp, url_prefix='/gas')

# blueprint for water part
from app.water import bp as water_bp
app.register_blueprint(water_bp, url_prefix='/water')

from app import routes
