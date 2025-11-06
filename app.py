from flask import Flask, redirect, url_for, current_app
import locale
from datetime import date, datetime, timedelta

from extensions import db, login_manager, migrate, mail

# --- Configuração de Locale ---
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
    except locale.Error:
        print("Aviso: Locale 'pt_BR' ou 'Portuguese_Brazil' não encontrado.")

# Blueprints - Importar apenas UMA vez
from blueprints.users import users_bp
from blueprints.tasks import tasks_bp
from blueprints.backup import backup_bp
from blueprints.reminders.routes import bp as reminders_bp
from blueprints.goals.routes import bp as goals_bp
from blueprints.profile.routes import bp as profile_bp

# Hub (opcional)
try:
    from blueprints.hub import hub_bp
except Exception:
    hub_bp = None


# --- Helper format_due_date ---
def format_due_date(due_date, is_done=False, completed_at=None):
    if is_done and completed_at:
        css_class = 'due-date-done'
        today = date.today()
        completed_date = completed_at.date()
        delta_completed = (completed_date - today).days
        if delta_completed == 0:
            text = f"Concluído: Hoje às {completed_at.strftime('%H:%M')}"
        elif delta_completed == -1:
            text = f"Concluído: Ontem às {completed_at.strftime('%H:%M')}"
        else:
            text = f"Concluído: {completed_at.strftime('%d/%m/%Y %H:%M')}"
    elif due_date:
        today = date.today()
        delta = (due_date - today).days
        css_class = 'due-date-default'
        text = f"Prazo: {due_date.strftime('%d/%m/%Y')}"
        
        if delta < 0:
            css_class = 'due-date-overdue'
            if delta == -1:
                text = "Prazo: Ontem"
            else:
                text = f"Prazo: Há {-delta} dias"
        elif delta == 0:
            css_class = 'due-date-today'
            text = "Prazo: Hoje"
        elif delta == 1:
            css_class = 'due-date-soon'
            text = "Prazo: Amanhã"
        elif delta <= 7:
            try:
                text = f"Prazo: {due_date.strftime('%A').capitalize()}"
                css_class = 'due-date-soon'
            except:
                text = f"Prazo: Em {delta} dias"
                css_class = 'due-date-future'
        else:
            text = f"Prazo: {due_date.strftime('%d de %b')}"
            css_class = 'due-date-future'
    else:
        return {'text': '', 'class': ''}
    
    return {'text': text, 'class': css_class}


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    
    # Carregar configurações
    app.config.from_object('config')
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    # --- Context Processors ---
    @app.context_processor
    def inject_helpers():
        def has_endpoint(name: str) -> bool:
            return name in current_app.view_functions
        
        def url_or(primary: str, fallback: str):
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
        
        return dict(
            has_endpoint=has_endpoint,
            url_or=url_or,
            first_name=first_name,
            format_due_date=format_due_date
        )
    
    # --- Registrar Blueprints (apenas UMA vez cada) ---
    app.register_blueprint(users_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(backup_bp)
    app.register_blueprint(reminders_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(profile_bp)
    
    # Hub é opcional
    if hub_bp:
        app.register_blueprint(hub_bp)
    
    # Rota raiz
    @app.get("/")
    def root():
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_or("hub.index", "tasks.index"))
        return redirect(url_for("users.login"))
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == "__main__":
    from waitress import serve
    application = create_app()
    assert application is not None, "create_app() retornou None"
    print("🚀 RoutineUp rodando em http://127.0.0.1:8000")
    serve(application, host="127.0.0.1", port=8000)