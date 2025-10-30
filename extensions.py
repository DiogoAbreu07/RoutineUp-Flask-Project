from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail # <-- Importa o Mail

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail() # <-- Cria a instância do Mail