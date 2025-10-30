from flask import Flask, redirect, url_for, current_app
import locale
from datetime import date, datetime, timedelta

# As configurações individuais não são mais importadas do config.py
# from config import (...)

# ALTERADO: Importa 'mail' junto com as outras extensões
from extensions import db, login_manager, migrate, mail

# --- Configuração de Locale (mantida) ---
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
    except locale.Error:
        print("Aviso: Locale 'pt_BR' ou 'Portuguese_Brazil' não encontrado. A data pode aparecer em inglês.")
# --- Fim Locale ---


# Blueprints (mantidos)
from blueprints.users import users_bp
from blueprints.tasks import tasks_bp
from blueprints.backup import backup_bp
try: from blueprints.hub import hub_bp
except Exception: hub_bp = None
try: from blueprints.goals import goals_bp
except Exception: goals_bp = None
try: from blueprints.reminders import reminders_bp
except Exception: reminders_bp = None
try: from blueprints.profile import profile_bp
except Exception: profile_bp = None

# --- Helper format_due_date (mantido) ---
def format_due_date(due_date, is_done=False, completed_at=None): # Adicionado completed_at
    if is_done and completed_at: # Se concluído E tem data de conclusão
        css_class = 'due-date-done'
        today = date.today()
        completed_date = completed_at.date()
        delta_completed = (completed_date - today).days
        if delta_completed == 0: text = f"Concluído: Hoje às {completed_at.strftime('%H:%M')}"
        elif delta_completed == -1: text = f"Concluído: Ontem às {completed_at.strftime('%H:%M')}"
        else: text = f"Concluído: {completed_at.strftime('%d/%m/%Y %H:%M')}"
    elif due_date: # Se não concluído, mas tem prazo
        today = date.today(); delta = (due_date - today).days
        css_class = 'due-date-default'; text = f"Prazo: {due_date.strftime('%d/%m/%Y')}"
        if delta < 0:
            css_class = 'due-date-overdue'
            if delta == -1: text = "Prazo: Ontem"
            else: text = f"Prazo: Há {-delta} dias"
        elif delta == 0: css_class = 'due-date-today'; text = "Prazo: Hoje"
        elif delta == 1: css_class = 'due-date-soon'; text = "Prazo: Amanhã"
        elif delta <= 7:
            try: text = f"Prazo: {due_date.strftime('%A').capitalize()}"; css_class = 'due-date-soon'
            except: text = f"Prazo: Em {delta} dias"; css_class = 'due-date-future'
        else: text = f"Prazo: {due_date.strftime('%d de %b')}"; css_class = 'due-date-future'
    else: return {'text': '', 'class': ''} # Sem prazo e não concluído
    return {'text': text, 'class': css_class}
# --- FIM DO HELPER ---


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # ALTERADO: Carrega todas as configurações de config.py (incluindo as de MAIL)
    app.config.from_object('config')

    # Extensões
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app) # <-- NOVO: Inicializa o Flask-Mail

    # --- HELPERS JINJA (mantidos) ---
    @app.context_processor
    def inject_helpers():
        def has_endpoint(name: str) -> bool:
            return name in current_app.view_functions
        def url_or(primary: str, fallback: str):
            try:
                if has_endpoint(primary): return url_for(primary)
            except Exception: pass
            try:
                if has_endpoint(fallback): return url_for(fallback)
            except Exception: pass
            return fallback
        def first_name(user):
            try:
                nm = (getattr(user, "name", "") or "").strip()
                return nm.split()[0] if nm else ""
            except Exception: return ""
        
        return dict(
            has_endpoint=has_endpoint,
            url_or=url_or,
            first_name=first_name,
            format_due_date=format_due_date
        )
    # --- FIM DOS HELPERS ---

    # Blueprints (mantidos)
    app.register_blueprint(users_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(backup_bp)
    if hub_bp: app.register_blueprint(hub_bp)
    if goals_bp: app.register_blueprint(goals_bp)
    if reminders_bp: app.register_blueprint(reminders_bp)
    if profile_bp: app.register_blueprint(profile_bp)

    # Rota raiz (mantida)
    @app.get("/")
    def root():
        from flask_login import current_user
        return redirect(url_or("hub.index", "users.login") if current_user.is_authenticated else url_for("users.login"))

    # Cria tabelas (mantido)
    with app.app_context():
        db.create_all()

    return app

# Bloco main (mantido)
if __name__ == "__main__":
    from waitress import serve
    application = create_app()
    assert application is not None, "create_app() retornou None — verifique o conteúdo do arquivo."
    serve(application, host="127.0.0.1", port=8000)