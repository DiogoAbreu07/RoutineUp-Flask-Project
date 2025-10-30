from app import create_app
from extensions import db
from models import User

TARGET_EMAIL = "coloque-seu-email@aqui.com"  # <<< edite
NEW_NAME     = "Seu Nome"                    # <<< edite

app = create_app()
with app.app_context():
    u = User.query.filter_by(email=TARGET_EMAIL.lower().strip()).first()
    if not u:
        print("Usuário não encontrado:", TARGET_EMAIL)
    else:
        u.name = NEW_NAME.strip()
        db.session.commit()
        print("OK! name atualizado para:", u.name)
