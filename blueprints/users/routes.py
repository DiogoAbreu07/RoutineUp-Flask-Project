from . import users_bp
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from extensions import db, login_manager
from models import User
import secrets

# -------- user loader exigido pelo Flask-Login --------
@login_manager.user_loader
def load_user(user_id: str):
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None
# ------------------------------------------------------

def _sanitize_email(s: str) -> str:
    return (s or "").strip().lower()

# Dicionário temporário para armazenar tokens de recuperação
# Em produção, use Redis ou salve no banco de dados
password_reset_tokens = {}

@users_bp.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("hub.index"))
    return render_template("users/login.html")

@users_bp.post("/login")
def login_post():
    email = _sanitize_email(request.form.get("email"))
    pw = request.form.get("password") or ""
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, pw):
        flash("Credenciais inválidas.", "error")
        return redirect(url_for("users.login"))
    remember = bool(request.form.get("remember"))
    login_user(user, remember=remember)
    return redirect(url_for("hub.index"))

@users_bp.get("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("hub.index"))
    return render_template("users/register.html")

@users_bp.post("/register")
def register_post():
    name  = (request.form.get("name") or "").strip()
    email = _sanitize_email(request.form.get("email"))
    pw    = request.form.get("password") or ""
    birth_raw = (request.form.get("birth_date") or "").strip()
    gender = (request.form.get("gender") or "").strip() or None

    if not name or len(name) < 2:
        flash("Informe um nome válido.", "error")
        return redirect(url_for("users.register"))
    if not email or "@" not in email:
        flash("Informe um e-mail válido.", "error")
        return redirect(url_for("users.register"))
    if len(pw) < 6:
        flash("A senha deve ter pelo menos 6 caracteres.", "error")
        return redirect(url_for("users.register"))
    if User.query.filter_by(email=email).first():
        flash("Já existe um usuário com este e-mail.", "error")
        return redirect(url_for("users.register"))

    birth_date = None
    if birth_raw:
        try:
            birth_date = datetime.strptime(birth_raw, "%Y-%m-%d").date()
        except ValueError:
            flash("Data de nascimento inválida.", "error")
            return redirect(url_for("users.register"))

    User.create(email=email, password=pw, name=name, birth_date=birth_date, gender=gender)
    flash("Conta criada com sucesso. Você já pode entrar.", "success")
    return redirect(url_for("users.login"))

@users_bp.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))

# ==================== NOVAS ROTAS: RECUPERAÇÃO DE SENHA ====================

@users_bp.get("/forgot-password")
def forgot_password():
    """Página para solicitar recuperação de senha"""
    if current_user.is_authenticated:
        return redirect(url_for("hub.index"))
    return render_template("users/forgot_password.html")

@users_bp.post("/forgot-password")
def forgot_password_post():
    """Processa solicitação de recuperação de senha"""
    email = _sanitize_email(request.form.get("email"))
    
    if not email or "@" not in email:
        flash("Por favor, informe um e-mail válido.", "error")
        return redirect(url_for("users.forgot_password"))
    
    user = User.query.filter_by(email=email).first()
    
    # Por segurança, sempre mostra mensagem de sucesso mesmo se email não existir
    if not user:
        flash("Se o e-mail estiver cadastrado, você receberá um link de recuperação.", "info")
        return redirect(url_for("users.login"))
    
    # Gera token único e seguro
    token = secrets.token_urlsafe(32)
    
    # Armazena token com expiração de 1 hora
    password_reset_tokens[token] = {
        'user_id': user.id,
        'email': email,
        'expires_at': datetime.utcnow() + timedelta(hours=1)
    }
    
    # Em produção, você enviaria um e-mail aqui
    # Por enquanto, vamos apenas gerar o link e mostrar no flash
    reset_link = url_for('users.reset_password', token=token, _external=True)
    
    # TEMPORÁRIO: Mostra o link direto (em produção, envie por e-mail)
    flash(f"Link de recuperação (TEMPORÁRIO - copie este link): {reset_link}", "success")
    
    # TODO: Implementar envio de e-mail real
    # send_password_reset_email(email, reset_link)
    
    print(f"\n{'='*60}")
    print(f"🔑 LINK DE RECUPERAÇÃO DE SENHA")
    print(f"{'='*60}")
    print(f"E-mail: {email}")
    print(f"Link: {reset_link}")
    print(f"Válido até: {password_reset_tokens[token]['expires_at']}")
    print(f"{'='*60}\n")
    
    return redirect(url_for("users.login"))

@users_bp.get("/reset-password/<token>")
def reset_password(token):
    """Página para redefinir senha com token"""
    if current_user.is_authenticated:
        return redirect(url_for("hub.index"))
    
    # Verifica se token existe
    if token not in password_reset_tokens:
        flash("Link de recuperação inválido ou expirado.", "error")
        return redirect(url_for("users.forgot_password"))
    
    # Verifica se token expirou
    token_data = password_reset_tokens[token]
    if datetime.utcnow() > token_data['expires_at']:
        del password_reset_tokens[token]
        flash("Este link expirou. Solicite um novo link de recuperação.", "error")
        return redirect(url_for("users.forgot_password"))
    
    return render_template("users/reset_password.html", token=token)

@users_bp.post("/reset-password/<token>")
def reset_password_post(token):
    """Processa redefinição de senha"""
    # Verifica token
    if token not in password_reset_tokens:
        flash("Link de recuperação inválido ou expirado.", "error")
        return redirect(url_for("users.forgot_password"))
    
    token_data = password_reset_tokens[token]
    if datetime.utcnow() > token_data['expires_at']:
        del password_reset_tokens[token]
        flash("Este link expirou. Solicite um novo link de recuperação.", "error")
        return redirect(url_for("users.forgot_password"))
    
    # Valida senhas
    password = request.form.get("password") or ""
    password_confirm = request.form.get("password_confirm") or ""
    
    if len(password) < 6:
        flash("A senha deve ter pelo menos 6 caracteres.", "error")
        return redirect(url_for("users.reset_password", token=token))
    
    if password != password_confirm:
        flash("As senhas não coincidem.", "error")
        return redirect(url_for("users.reset_password", token=token))
    
    # Busca usuário e atualiza senha
    user = User.query.get(token_data['user_id'])
    if not user:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for("users.forgot_password"))
    
    # Atualiza senha
    user.password_hash = generate_password_hash(password)
    db.session.commit()
    
    # Remove token usado
    del password_reset_tokens[token]
    
    flash("Senha redefinida com sucesso! Você já pode fazer login.", "success")
    return redirect(url_for("users.login"))