from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from controllers.home import home_bp
from controllers.auth import auth_bp
from controllers.dashboard import dashboard_bp
from controllers.api import api_bp
from config import Config
from models import db
from models.user import User
from flask_login import LoginManager

# Configurações
app = Flask(__name__, template_folder='views', static_folder='static')
app.config.from_object(Config)
db.init_app(app)

# Registrando os Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(api_bp)

# Inicializa o LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# login padrão
login_manager.login_view = 'auth.login'

# Carrega o usuário com base no ID armazenado na sessão
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Inicia
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados se não existirem
    app.run(host='0.0.0.0', port=5000)
