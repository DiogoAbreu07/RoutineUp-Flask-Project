from flask import Flask, redirect, url_for
from config import (
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
    MAX_CONTENT_LENGTH,
)
from extensions import db, login_manager, migrate

# Blueprints (alguns podem não existir em ambiente parcial; tratamos o hub como opcional)
from blueprints.users import users_bp
from blueprints.tasks import tasks_bp
from blueprints.backup import backup_bp
try:
    from blueprints.hub import hub_bp
except Exception:
    hub_bp = None


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Config
    app.config.update(
        SECRET_KEY=SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=SQLALCHEMY_TRACK_MODIFICATIONS,
        MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH,
    )

    # Extensões
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Helpers do Jinja
    def has_endpoint(name: str) -> bool:
        from flask import current_app
        return name in current_app.view_functions

    def url_or(primary: str, fallback: str):
        # Tenta construir a URL do endpoint primário; se não der, tenta o fallback;
        # se também não existir, devolve a string fallback (ex: "/").
        from flask import current_app, url_for
        try:
            if has_endpoint(primary):
                return url_for(primary)
        except Exception:
            pass
        try:
            if has_endpoint(fallback):
                return url_for(fallback)
        except Exception:
            pass
        return fallback

    

    def first_name(user):
        try:
            nm = (getattr(user, "name", "") or "").strip()
            return nm.split()[0] if nm else ""
        except Exception:
            return ""
    app.jinja_env.globals.update(has_endpoint=has_endpoint, url_or=url_or, first_name=first_name)

    # Blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(backup_bp)
    if hub_bp:
        app.register_blueprint(hub_bp)

    # Rota raiz
    @app.get("/")
    def root():
        from flask_login import current_user
        # Vai para o hub se logado; senão, tela de login
        return redirect(url_for("hub.index") if has_endpoint("hub.index") and current_user.is_authenticated
                        else url_for("users.login"))

    # Cria tabelas (se ainda não existirem)
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    from waitress import serve
    application = create_app()
    assert application is not None, "create_app() retornou None — verifique o conteúdo do arquivo."
    serve(application, host="127.0.0.1", port=8000)

